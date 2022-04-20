from openupgradelib import openupgrade
from psycopg2 import sql
import logging

_logger = logging.getLogger(__name__)

def update_account_move_cdfi_invoice_fields(cr):
    openupgrade.logged_query(
        cr, """
            UPDATE account_move am
            SET factura_cfdi = ai.factura_cfdi,
            tipo_comprobante = ai.tipo_comprobante,
            forma_pago = ai.forma_pago,
            methodo_pago = ai.methodo_pago,
            uso_cfdi = ai.uso_cfdi,
            estado_factura = ai.estado_factura,
            tipocambio = ai.tipocambio,
            moneda = ai.moneda,
            qr_value = ai.qr_value,
            tipo_relacion = ai.tipo_relacion,
            uuid_relacionado = ai.uuid_relacionado,
            folio_fiscal = ai.folio_fiscal
            FROM account_invoice ai
            WHERE am.old_invoice_id = ai.id
            """
    )

def update_res_partner_cdfi_fields(cr):
    openupgrade.logged_query(
        cr, """
            UPDATE res_partner rp
            SET vat = rp_old.rfc
            FROM res_partner rp_old
            """
    )
def update_product_clave_unidad_field(cr):
    openupgrade.logged_query(
        cr, """
            UPDATE product_template tmpl
            SET cat_unidad_medida = catalogo.id
            FROM product_template t
            left join catalogo_unidad_medida catalogo on catalogo.descripcion=t.unidad_medida
            """
    )
    
@openupgrade.migrate()
def migrate(env, version):
    update_account_move_cdfi_invoice_fields(env.cr)
    update_res_partner_cdfi_fields(env.cr)
    update_product_clave_unidad_field(env.cr)
    
