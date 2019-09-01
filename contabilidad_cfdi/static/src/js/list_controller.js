odoo.define('contabilidad_cfdi.ListController', function (require) {
"use strict";

var ListController = require('web.ListController');
var session = require('web.session');
var crash_manager = require('web.crash_manager');

ListController.include({
	renderButtons: function ($node) {
		this._super($node)
		/*if (this.modelName==='account.account' && !this.noLeaf && this.hasButtons){
			var context = this.model.get(this.handle, {raw: true}).getContext();
			if (context.is_catalogo_de_cuentas!==undefined && context.is_catalogo_de_cuentas==true){
				if (this.$buttons.find(".o_list_button_discard").length){
					var $export_xls_button = $("<button type='button' class='btn btn-default btn-sm o_list_button_export_coa_sat' accesskey='co'>Exportar XLS</button>");
					var $export_xml_button = $("<button type='button' class='btn btn-default btn-sm o_list_button_export_coa_xml_sat' accesskey='xm'>Generar XML</button>");
					this.$buttons.find(".o_list_button_discard").after($export_xml_button);
					this.$buttons.find(".o_list_button_discard").after($export_xls_button);
					this.$buttons.on('click', '.o_list_button_export_coa_sat', this._onExportSatAccount.bind(this));
					this.$buttons.on('click', '.o_list_button_export_coa_xml_sat', this._onGenerarXMLAccount.bind(this));
				}
			}
		}*/
		if (this.modelName==='reporte.diot.wizard.line' && !this.noLeaf && this.hasButtons){
			if (this.$buttons.find(".o_list_button_discard").length){
				var $export_xls_button = $("<button type='button' class='btn btn-default btn-sm o_list_button_export_xls_diot' accesskey='diotxls'>XLS</button>");
				var $export_txt_button = $("<button type='button' class='btn btn-default btn-sm o_list_button_export_txt_diot' accesskey='diotxm'>TXT</button>");
				this.$buttons.find(".o_list_button_discard").after($export_xls_button);
				this.$buttons.find(".o_list_button_discard").after($export_txt_button);
				this.$buttons.on('click', '.o_list_button_export_xls_diot', this._onExportDIOTXLS.bind(this));
				this.$buttons.on('click', '.o_list_button_export_txt_diot', this._onExportDIOTTXT.bind(this));
			}
		}
	},
	_onExportDIOTXLS: function (event) {
		event.stopPropagation();
        var self = this;
        var res_ids = this.model.get(this.handle, {raw: true}).res_ids;
        var c = crash_manager;        
        session.get_file({
            url: '/web/export/xls_txt_diot_download',
            data: {record_ids: JSON.stringify(res_ids),report_type:'xls'},
            complete: $.unblockUI,
            error: c.rpc_error.bind(c)
        });
	},
	_onExportDIOTTXT: function (event) {
		event.stopPropagation();
        var self = this;
        var res_ids = this.model.get(this.handle, {raw: true}).res_ids;
        var c = crash_manager;        
        session.get_file({
            url: '/web/export/xls_txt_diot_download',
            data: {record_ids: JSON.stringify(res_ids),report_type:'txt'},
            complete: $.unblockUI,
            error: c.rpc_error.bind(c)
        });
	},
	_onGenerarXMLAccount: function (event) {
        event.stopPropagation();
        var self = this;
        return this.do_action({
            name: "Generar XML",
            type: 'ir.actions.act_window',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_model: 'generar.xml.wizard'
        });
        /*var c = crash_manager;        
        session.get_file({
            url: '/web/export/xml_account_view',
            complete: $.unblockUI,
            error: c.rpc_error.bind(c)
        });*/ 
    },
    /*_onExportSatAccount: function (event) {
        event.stopPropagation();
        var c = crash_manager;        
        session.get_file({
            url: '/web/export/xls_account_view',
            complete: $.unblockUI,
            error: c.rpc_error.bind(c)
        });
        
        
    },*/
});

});