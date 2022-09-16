frappe.ui.form.on('Task', {
	refresh:function(frm){
		var task_list= []
		$.each(frm.doc.depends_on,function(index,row){
		     if (row.task){
                task_list.push(row.task)
		     }
        })
        if(task_list.length > 0){
        	frappe.call({
	            method: "pms.pms.custom_script.task.check_task_status",
	            args: {"task_list": task_list},
	            callback: function(r) {
	                if(r.message) {
                        frm.add_custom_button(__('Material Request'), function() {
	                        frappe.model.open_mapped_doc({
								method: "pms.pms.custom_script.task.make_material_request",
								frm: frm
							});
						})
	                }
	            }
	        });
        }
        else if (task_list.length == 0){
        	frm.add_custom_button(__('Material Request'), function() {
				frappe.model.open_mapped_doc({
					method: "pms.pms.custom_script.task.make_material_request",
					frm: frm
				});
			})
        }
	}
})


