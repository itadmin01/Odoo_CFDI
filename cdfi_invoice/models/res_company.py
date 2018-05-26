# -*- coding: utf-8 -*-

from odoo import fields, models, api,_

class ResCompany(models.Model):
    _inherit = 'res.company'

    rfc = fields.Char(string=_('RFC'))
    proveedor_timbrado= fields.Selection(
        selection=[('gecoerp', _('GecoERP')),
                   ('multifactura', _('Multifacturas')),],
        string=_('Proveedor de timbrado'), 
    )
    api_key = fields.Char(string=_('API Key'))
    http_factura = fields.Char(string=_('HTTP Factura'))
    factura_dir = fields.Char(string=_('Directorio XML'))
    modo_prueba = fields.Boolean(string=_('Modo prueba'))
    serie_factura = fields.Char(string=_('Serie factura'))
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
                   ('615', _('Régimen de los ingresos por obtención de premios')),],
        string=_('Régimen Fiscal'), 
    )
    archivo_cer = fields.Binary(string=_('Archivo .cer'))
    archivo_key = fields.Binary(string=_('Archivo .key'))
    contrasena = fields.Char(string=_('Contraseña'))
    nombre_fiscal = fields.Char(string=_('Razón social'))
    serie_complemento = fields.Char(string=_('Serie complemento de pago'))
    telefono_sms = fields.Char(string=_('Teléfono celular'))