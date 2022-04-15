# -*- coding: utf-8 -*-

from odoo import fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    residencia_fiscal = fields.Char(string=_('Residencia Fiscal'))
    registro_tributario = fields.Char(string=_('Registro tributario'))
    uso_cfdi = fields.Selection(
        selection=[('G01', _('Adquisición de mercancías')),
                   ('G02', _('Devoluciones, descuentos o bonificaciones')),
                   ('G03', _('Gastos en general')),
                   ('I01', _('Construcciones')),
                   ('I02', _('Mobiliario y equipo de oficina por inversiones')),
                   ('I03', _('Equipo de transporte')),
                   ('I04', _('Equipo de cómputo y accesorios')),
                   ('I05', _('Dados, troqueles, moldes, matrices y herramental')),
                   ('I06', _('Comunicacion telefónica')),
                   ('I07', _('Comunicación Satelital')),
                   ('I08', _('Otra maquinaria y equipo')),
                   ('D01', _('Honorarios médicos, dentales y gastos hospitalarios')),
                   ('D02', _('Gastos médicos por incapacidad o discapacidad')),
                   ('D03', _('Gastos funerales')),
                   ('D04', _('Donativos')),
                   ('D05', _('Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación).')),
                   ('D06', _('Aportaciones voluntarias al SAR.')),
                   ('D07', _('Primas por seguros de gastos médicos')),
                   ('D08', _('Gastos de transportación escolar obligatoria')),
                   ('D09', _('Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones')),
                   ('D10', _('Pagos por servicios educativos (colegiaturas)')),
                   ('S01', _('Sin efectos fiscales')),
                   ('P01', _('Por definir (obsoleto)')),],
        string=_('Uso CFDI (cliente)'),
    )
    regimen_fiscal = fields.Selection(
        selection=[('601', _('General de Ley Personas Morales')),
                   ('603', _('Personas Morales con Fines no Lucrativos')),
                   ('605', _('Sueldos y Salarios e Ingresos Asimilados a Salarios')),
                   ('606', _('Arrendamiento')),
                   ('608', _('Demás ingresos')),
                   ('609', _('Consolidación')),
                   ('610', _('Residentes en el Extranjero sin Establecimiento Permanente en México')),
                   ('611', _('Ingresos por Dividendos (socios y accionistas)')),
                   ('612', _('Personas Físicas con Actividades Empresariales y Profesionales')),
                   ('614', _('Ingresos por intereses')),
                   ('616', _('Sin obligaciones fiscales')),
                   ('620', _('Sociedades Cooperativas de Producción que optan por diferir sus ingresos')),
                   ('621', _('Incorporación Fiscal')),
                   ('622', _('Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras')),
                   ('623', _('Opcional para Grupos de Sociedades')),
                   ('624', _('Coordinados')),
                   ('628', _('Hidrocarburos')),
                   ('607', _('Régimen de Enajenación o Adquisición de Bienes')),
                   ('629', _('De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales')),
                   ('630', _('Enajenación de acciones en bolsa de valores')),
                   ('615', _('Régimen de los ingresos por obtención de premios')),
                   ('625', _('Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas')),
                   ('626', _('Régimen Simplificado de Confianza')),],
        string=_('Régimen Fiscal'), 
    )

    def check_vat(self):
        if self.env.context.get('company_id'):
            company = self.env['res.company'].browse(self.env.context['company_id'])
        else:
            company = self.env.company
        if company.vat_check_vies:
            # force full VIES online check
            check_func = self.vies_vat_check
        else:
            # quick and partial off-line checksum validation
            check_func = self.simple_vat_check
        for partner in self:
            if not partner.vat:
                continue
            #check with country code as prefix of the TIN
            vat_country, vat_number = self._split_vat(partner.vat)
            if not check_func(vat_country, vat_number):
                #if fails, check with country code from country
                country_code = 'MX' #partner.commercial_partner_id.country_id.code
                if country_code:
                    if not check_func(country_code.lower(), partner.vat):
                        msg = partner._construct_constraint_msg(country_code.lower())
                        raise ValidationError(msg)
