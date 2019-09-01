odoo.define('contabilidad_cfdi.ir_actions_act_multi_print', function (require) {
"use strict";

    var ActionManager = require('web.ActionManager');
    
    ActionManager.include({

        execute_ir_actions_act_multi_print: function(actions, options, index){
            var self = this;

            var i = 0;
            for(i=0;i<actions.length;i++)
            	{
            	var popup = actions[i].target === 'new';
                var inline = actions[i].target === 'inline' || actions[i].target === 'inlineview';
                var form = _.str.startsWith(actions[i].view_mode, 'form');
                actions[i].flags = _.defaults(actions[i].flags || {}, {
                    views_switcher : !popup && !inline,
                    search_view : !(popup && form) && !inline,
                    action_buttons : !popup && !inline,
                    sidebar : !popup && !inline,
                    pager : (!popup || !form) && !inline,
                    display_title : !popup,
                    headless: (popup || inline) && form,
                    search_disable_custom_filters: actions[i].context && actions[i].context.search_disable_custom_filters,
                });
                
            	if (actions[i].type=='ir.actions.act_url'){
            		self.ir_actions_act_url(actions[i],options);
            	}
            	else if(actions[i].type=='ir.actions.act_window'){
            		self.ir_actions_act_window(actions[i],options)
            	}
            	
            	}
            return true;
        },

        ir_actions_act_multi_print: function(action, options){
            return this.execute_ir_actions_act_multi_print(action.actions, options, 0);
        },
        

    });
    
});
