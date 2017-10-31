# -*- coding: utf-8 -*-
import json
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
from openerp.tools import float_is_zero

from openerp.exceptions import ValidationError, RedirectWarning, ValidationError

import openerp.addons.decimal_precision as dp
import amount_to_text_es_MX

def formatLang(env, value, digits=None, grouping=True, monetary=False, dp=False, currency_obj=False):
    """
        Assuming 'Account' decimal.precision=3:
            formatLang(value) -> digits=2 (default)
            formatLang(value, digits=4) -> digits=4
            formatLang(value, dp='Account') -> digits=3
            formatLang(value, digits=5, dp='Account') -> digits=5
    """

    if digits is None:
        digits = DEFAULT_DIGITS = 2
        if dp:
            decimal_precision_obj = env['decimal.precision']
            digits = decimal_precision_obj.precision_get(dp)
        elif (hasattr(value, '_field') and isinstance(value._field, (float_field, function_field)) and value._field.digits):
                digits = value._field.digits[1]
                if not digits and digits is not 0:
                    digits = DEFAULT_DIGITS

    if isinstance(value, (str, unicode)) and not value:
        return ''

    lang = env.user.company_id.partner_id.lang or 'en_US'
    lang_objs = env['res.lang'].search([('code', '=', lang)])
    if not lang_objs:
        lang_objs = env['res.lang'].search([('code', '=', 'en_US')])
    lang_obj = lang_objs[0]

    res = lang_obj.format('%.' + str(digits) + 'f', value, grouping=grouping, monetary=monetary)

    if currency_obj:
        if currency_obj.position == 'after':
            res = '%s %s' % (res, currency_obj.symbol)
        elif currency_obj and currency_obj.position == 'before':
            res = '%s %s' % (currency_obj.symbol, res)
    return res
#----------------------------------------------------------
# Incoterms
#----------------------------------------------------------
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    forma_pago = fields.Selection(
        selection=[('01', '01 - Efectivo'), 
                   ('02', '02 - Cheque nominativo'), 
                   ('03', '03 - Transferencia electrónica de fondos'),
                   ('04', '04 - Tarjeta de Crédito'), 
                   ('05', '05 - Monedero electrónico'),
                   ('06', '06 - Dinero electrónico'), 
                   ('08', '08 - Vales de despensa'), 
                   ('12', '12 - Dación en pago'), 
                   ('13', '13 - Pago por subrogación'), 
                   ('14', '14 - Pago por consignación'), 
                   ('15', '15 - Condonación'), 
                   ('17', '17 - Compensación'), 
                   ('23', '23 - Novación'), 
                   ('24', '24 - Confusión'), 
                   ('25', '25 - Remisión de deuda'), 
                   ('26', '26 - Prescripción o caducidad'), 
                   ('27', '27 - A satisfacción del acreedor'), 
                   ('28', '28 - Tarjeta de débito'), 
                   ('29', '29 - Tarjeta de servicios'),
                   ('30', '30 - Aplicación de anticipos'), 				   
                   ('99', '99 - Por definir'),],
        string=_('Forma de pago'),
    )
    #num_cta_pago = fields.Char(string=_('Núm. Cta. Pago'))
    methodo_pago = fields.Selection(
        selection=[('PUE', _('Pago en una sola exhibición')),
		           ('PPD', _('Pago en parcialidades o diferido')),],
        string=_('Método de pago'), 
    )
    uso_cfdi = fields.Selection(
        selection=[('G01', _('Adquisición de mercancías')),
                   ('G02', _('Devoluciones, descuentos o bonificaciones')),
                   ('G03', _('Gastos en general')),
                   ('I01', _('Construcciones')),
                   ('I02', _('Mobiliario y equipo de oficina por inversiones')),
                   ('I03', _('Equipo de transporte')),
                   ('I04', _('Equipo de cómputo y accesorios')),
                   ('I05', _('Dados, troqueles, moldes, matrices y herramental')),
                   ('I08', _('Otra maquinaria y equipo')),
                   ('D01', _('Honorarios médicos, dentales y gastos hospitalarios')),
                   ('D02', _('Gastos médicos por incapacidad o discapacidad')),
                   ('D03', _('Gastos funerales')),
                   ('D04', _('Donativos')),
                   ('D07', _('Primas por seguros de gastos médicos')),
                   ('D08', _('Gastos de transportación escolar obligatoria')),
                   ('D10', _('Pagos por servicios educativos (colegiaturas)')),
                   ('P01', _('Por definir')),],
        string=_('Uso CFDI (cliente)'),
    )
     
    @api.depends('amount_total', 'currency_id')
    @api.one
    def _get_amount_to_text(self):
        self.amount_to_text = amount_to_text_es_MX.get_amount_to_text(self, self.amount_total, 'es_cheque', self.currency_id.name)
        
    @api.model
    def _get_amount_2_text(self, amount_total):
        return amount_to_text_es_MX.get_amount_to_text(self, amount_total, 'es_cheque', self.currency_id.name)
        
    @api.model
    def _prepare_invoice(self, order, lines):
        invoice_vals = super(SaleOrder, self)._prepare_invoice(order, lines)
        invoice_vals.update({'forma_pago': order.forma_pago,
                    'methodo_pago': order.methodo_pago,
                    'uso_cfdi': order.uso_cfdi,
                    'tipo_comprobante': 'I'					
                    })
        return invoice_vals
    
    
    @api.multi
    def _get_tax_amount_by_group(self):
        self.ensure_one()
        res = {}
        currency = self.currency_id or self.company_id.currency_id
        for line in self.order_line:
            for tax in line.tax_id:
                group = tax
                res.setdefault(group, 0.0)
                res[group] += tax.compute_all(line.price_reduce, quantity=line.product_uom_qty)['taxes'][0]['amount']
        res = sorted(res.items(), key=lambda l: l[0].sequence)
        res = map(lambda l: (l[0].name, formatLang(self.env, l[1], currency_obj=currency)), res)
        return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
