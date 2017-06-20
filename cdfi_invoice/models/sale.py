# -*- coding: utf-8 -*-
import json
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
from openerp.tools import float_is_zero
from openerp.tools.misc import formatLang

from openerp.exceptions import UserError, RedirectWarning, ValidationError

import openerp.addons.decimal_precision as dp

#----------------------------------------------------------
# Incoterms
#----------------------------------------------------------
class sale_discount(models.Model):
    _inherit = 'sale.order'
    discount_value= fields.Float('Discount Amount', digits=(16, 2))
    discount_type= fields.Selection([('fixed', 'Fixed'),
                                      ('percent', 'Percentage'),],'Discount Type')
    discount_total = fields.Monetary(string='Discount', store=False, readonly=True, compute='_amount_all', track_visibility='always')
    amount_after_discount = fields.Monetary(string='Amount after discount',
        store=False, readonly=True, compute='_amount_all')
    @api.multi
    def button_dummy(self):
        return True

    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """       
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            discount_value=0
            if self.discount_type=='fixed':
                discount_value = self.discount_value
            elif self.discount_type=='percent':
                discount_value = (self.discount_value/100.0)*amount_untaxed

            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax - discount_value,
                'discount_total': discount_value,
                'amount_after_discount': amount_untaxed - discount_value,
            })
            print discount_value
    @api.multi
    def _prepare_invoice(self):
        res = super(sale_discount, self)._prepare_invoice()
        res['discount_type'] = self.discount_type
        res['discount_value'] = self.discount_value
        return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
