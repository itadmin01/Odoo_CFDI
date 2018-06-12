# -*- coding: utf-8 -*-
##############################################################################
#                 @author Esousy
#
##############################################################################

{
    'name': 'Catalogos para timbrado CFDI 3.3',
    'version': '1.0',
    'description': ''' Agrega catalogos para realizar el timbrado de facturas CFDI 3.3
    ''',
    'category': 'Accounting',
    'author': 'IT Admin',
    'website': 'www.itadmin.com.mx',
    'depends': [
        'base','sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/paises_view.xml',
        'data/catalogos.paises.csv',
        'views/colonia_view.xml',
        'data/catalogos.colonias.csv',		
        'views/estados_view.xml',
        'data/catalogos.estados.csv',
        'views/localidades_view.xml',
        'data/catalogos.localidades.csv',	
        'views/municipio_view.xml',
        'data/catalogos.municipio.csv',
        'views/clave_unidad_view.xml',
        'data/catalogos.clave_unidad.csv',
        'views/clave_prodserv_view.xml',
        'data/catalogos.claveprodserv.csv',	
        'views/fraccion_arancelaria.xml',
        'data/catalogos.fraccionarancelaria.csv',
        'views/unidad_medida_aduana.xml',
        'data/catalogos.unidadmedidaaduana.csv',
        'views/banco_view.xml',
        'data/catalogos.banco.csv',
	],
    'application': False,
    'installable': True,
}
