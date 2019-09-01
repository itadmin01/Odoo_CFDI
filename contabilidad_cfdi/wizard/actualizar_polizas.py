
from odoo import models, fields, api

class ActualizarPolizas(models.TransientModel):
    _name = 'actualizar.polizas'
    
    fecha_inicio = fields.Date('Fecha inicio')
    fecha_fin = fields.Date('Fecha fin')
    polizas_de_facturas_de_cliente = fields.Boolean('Polizas de facturas de cliente')
    polizas_de_facturas_de_proveedor = fields.Boolean('Polizas de facturas de proveedor')
    polizas_de_facturas_de_pagos = fields.Boolean('Polizas de facturas de pagos')
    polizas_de_inventarios = fields.Boolean('Polizas de inventarios')
    polizas_de_micelaneos = fields.Boolean('Polizas de micelaneos')
    
    @api.multi
    def action_validar_actualizar_polizas(self):
        if self.polizas_de_facturas_de_cliente:
            invoices = self.env['account.invoice'].search([('date_invoice','>=',self.fecha_inicio),
                                                           ('date_invoice','<=', self.fecha_fin),
                                                           ('estado_factura','=','factura_correcta'),
                                                           ('state','in', ['open', 'paid']),
                                                           ('type', '=', 'out_invoice')])
            moves = invoices.mapped('move_id')
            if moves:
                moves.write({'contabilidad_electronica':True})
                moves.mapped('line_ids').write({'contabilidad_electronica':True})
            cfdi_obj = self.env['account.move.cfdi33']
            for inv in invoices:
                move = inv.move_id
                if move:
                    cfdi_obj.create({'move_id': move.id,'fecha': inv.date_invoice, 'folio': inv.name, 'uuid': inv.folio_fiscal, 'partner_id': inv.partner_id.id, 'monto': inv.amount_total})
        if self.polizas_de_facturas_de_proveedor:
            invoices = self.env['account.invoice'].search([('date_invoice','>=',self.fecha_inicio),
                                                           ('date_invoice','<=', self.fecha_fin),
                                                           ('estado_factura','=','factura_correcta'),
                                                           ('state','in', ['open', 'paid']),
                                                           ('type', '=', 'in_invoice')])
            
            moves = invoices.mapped('move_id')
            if moves:
                moves.write({'contabilidad_electronica':True})
                moves.mapped('line_ids').write({'contabilidad_electronica':True})
            cfdi_obj = self.env['account.move.cfdi33']
            for inv in invoices:
                move = inv.move_id
                if move:
                    cfdi_obj.create({'move_id': move.id,'fecha': inv.date_invoice, 'folio': inv.name, 'uuid': inv.folio_fiscal, 'partner_id': inv.partner_id.id, 'monto': inv.amount_total})            
        
        if self.polizas_de_facturas_de_pagos:
            payments = self.env['account.payment'].search([('payment_date','>=',self.fecha_inicio),
                                                           ('payment_date','<=', self.fecha_fin),
                                                           ('estado_pago','=','pago_correcto'),
                                                           ('state','not in', ['draft', 'cancelled'])
                                                           ])
            
            move_lines = payments.mapped('move_line_ids')
            if move_lines:
                move_lines.write({'contabilidad_electronica':True})
                move_lines.mapped('move_id').write({'contabilidad_electronica':True})
            cfdi_obj = self.env['account.move.cfdi33']
            for payment in payments:
                for move in payment.move_line_ids.mapped('move_id'):
                    cfdi_obj.create({'move_id': move.id,'fecha': payment.fecha_pago, 'folio': payment.name, 'uuid': payment.folio_fiscal, 'partner_id': payment.partner_id.id, 'monto': payment.amount})
        if self.polizas_de_micelaneos:
            moves = self.env['account.move'].search([('date','>=',self.fecha_inicio),
                                             ('date','<=', self.fecha_fin),
                                             ('journal_id.type','=','general'),
                                             ])
            if moves:
                moves.write({'contabilidad_electronica':True})
                moves.mapped('line_ids').write({'contabilidad_electronica':True})
            
        return True