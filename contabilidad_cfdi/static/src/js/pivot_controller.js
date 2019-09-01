odoo.define('contabilidad_cfdi.PivotController', function (require) {
"use strict";

var PivotController = require('web.PivotController');
var crash_manager = require('web.crash_manager');
var framework = require('web.framework');
var session = require('web.session');

PivotController.include({
	renderButtons: function ($node) {
		this._super($node)
		if ($node && this.modelName==='account.hierarchy' && !this.noLeaf){
			//var context = this.model.get(this.handle, {raw: true}).getContext();
			var context = this.model.get(this.handle, {raw: true}).context
			if (context.show_xml_button!==undefined && context.show_xml_button==true){
				if (this.$buttons.find(".o_pivot_download").length){
					
					var $export_xml_button = $("<button type='button' class='btn btn-default o_pivot_download_xml'>XML</button>");
					this.$buttons.find(".o_pivot_download").after($export_xml_button);
				}
			}
		}
	},
	
	_onButtonClick: function (event) {
		var $target = $(event.target);
		if ($target.hasClass('o_pivot_download_xml')) {
            this._downloadXMLTable();
        }
		else{
			this._super(event);
		}
	},
	_downloadXMLTable: function () {
        var table = this.model.exportData();
        return this.do_action({
            name: "Generar XML",
            type: 'ir.actions.act_window',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_model: 'generar.xml.hirarchy.wizard',
            context: {data: JSON.stringify(table)}
        });
        
        
        /*table.title = this.title;
        session.get_file({
            url: '/web/pivot/export_xml',
            data: {data: JSON.stringify(table)},
            complete: framework.unblockUI,
            error: crash_manager.rpc_error.bind(crash_manager)
        });*/
    },
	
});

});