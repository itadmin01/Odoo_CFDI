# -*- coding: utf-8 -*-

from odoo import models,fields
from odoo.exceptions import Warning
import os
from lxml import etree
import base64
import json, xmltodict
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from dateutil.parser import parse
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib.units import mm

class import_account_payment_from_xml(models.TransientModel):
    _name ='import.account.payment.from.xml'

    import_file = fields.Binary("Importar Archivo",required=False)
    file_name = fields.Char("Nombre del archivo")
    payment_id = fields.Many2one("account.payment",'Payment')
    
    
    def import_xml_file_button(self):
        self.ensure_one()
        if not self.import_file:
            raise Warning("Seleccione primero el archivo.")
        p, ext = os.path.splitext(self.file_name)
        if ext[1:].lower() !='xml':
            raise Warning(_("Formato no soportado \"{}\", importa solo archivos XML").format(self.file_name))
        
        file_content = base64.b64decode(self.import_file)
        tree = etree.fromstring(file_content)
        payment_vals = {
            'cep_sello': tree.get('sello'),
            'cep_numeroCertificado' : tree.get('numeroCertificado',tree.get('NumeroCertificado')),
            'cep_cadenaCDA' : tree.get('cadenaCDA',tree.get('CadenaCDA')),
            'cep_claveSPEI' : tree.get('ClaveSPEI',tree.get('claveSPEI')),
            }
        self.payment_id.write(payment_vals)
        return True
    
    def import_xml_file_button_cargar(self):
        self.ensure_one()
        invoice_id = self.env['account.invoice'].browse(self._context.get('active_id'))
        if not self.import_file:
            raise Warning("Seleccione primero el archivo.")
        p, ext = os.path.splitext(self.file_name)
        if ext[1:].lower() !='xml':
            raise Warning(_("Formato no soportado \"{}\", importa solo archivos XML").format(self.file_name))
        
        file_coontent = base64.b64decode(self.import_file)
        file_coontent = file_coontent.replace(b'cfdi:',b'')
        file_coontent = file_coontent.replace(b'tfd:',b'')
        try:
            data = json.dumps(xmltodict.parse(file_coontent)) #force_list=('Concepto','Traslado',)
            data = json.loads(data)
        except Exception as e:
            data = {}
            raise Warning(str(e))

        timbrado_data = data.get('Comprobante',{}).get('Complemento',{}).get('TimbreFiscalDigital',{})
        receptor_data = data.get('Comprobante',{}).get('Receptor',{})
        xml_file_link = invoice_id.company_id.factura_dir + '/' + invoice_id.number.replace('/', '_') + '.xml'

        amount_str = str( data.get('Comprobante',{}).get('@Total',{})).split('.')
        qr_value = 'https://verificacfdi.facturaelectronica.sat.gob.mx/default.aspx?&id=%s&re=%s&rr=%s&tt=%s.%s&fe=%s' % (timbrado_data.get('@UUID'),
                                                 invoice_id.company_id.rfc, 
                                                 invoice_id.partner_id.rfc,
                                                 amount_str[0].zfill(10),
                                                 amount_str[1].ljust(6, '0'),
                                                 timbrado_data.get('@SelloCFD',{})[-8:],
                                                 )
        options = {'width': 275 * mm, 'height': 275 * mm}
        ret_val = createBarcodeDrawing('QR', value=qr_value, **options)
        qrcode_image = base64.encodestring(ret_val.asString('jpg'))

        cargar_values = {
            'methodo_pago': data.get('Comprobante',{}).get('@MetodoPago',{}),
            'forma_pago' : data.get('Comprobante',{}).get('@FormaPago',{}), 
            'uso_cfdi': receptor_data.get('@UsoCFDI'),
            'folio_fiscal' : timbrado_data.get('@UUID'),
            'tipo_comprobante': data.get('Comprobante',{}).get('@TipoDeComprobante',{}),
            'fecha_factura': timbrado_data.get('@FechaTimbrado') and parse(timbrado_data.get('@FechaTimbrado')).strftime(DEFAULT_SERVER_DATETIME_FORMAT) or False,
            'xml_invoice_link': xml_file_link,
            'factura_cfdi': True,
            'estado_factura': 'factura_correcta',
            'numero_cetificado' : data.get('Comprobante',{}).get('@NoCertificado',{}),
            'cetificaso_sat' : timbrado_data.get('@NoCertificadoSAT',{}),
            'fecha_certificacion' : timbrado_data.get('@FechaTimbrado',{}),
            'selo_digital_cdfi' : timbrado_data.get('@SelloCFD',{}),
            'selo_sat' : timbrado_data.get('@SelloSAT',{}),
            'tipocambio' : data.get('Comprobante',{}).get('@TipoCambio',{}),
            'moneda': data.get('Comprobante',{}).get('@Moneda',{}),
            'number_folio': data.get('Comprobante',{}).get('@Folio',{}),
            'cadena_origenal' : '||%s|%s|%s|%s|%s||' % (timbrado_data.get('@Version',{}), timbrado_data.get('@UUID',{}), timbrado_data.get('@FechaTimbrado',{}),
                                                         timbrado_data.get('@SelloCFD',{}), timbrado_data.get('@NoCertificadoSAT',{})),
            'qrcode_image': qrcode_image
            }
        invoice_id.write(cargar_values)

        xml_file = open(xml_file_link, 'w')
        xml_invoice = base64.b64decode(self.import_file)
        xml_file.write(xml_invoice.decode("utf-8"))
        xml_file.close()

        return True


