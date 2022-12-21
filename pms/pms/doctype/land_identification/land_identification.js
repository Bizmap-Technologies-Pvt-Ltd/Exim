// Copyright (c) 2022, bizmap tech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Land Identification', {
	refresh: function(frm) {
		if (frm.doc.land_status === 'Success'){
		frm.add_custom_button(__('Borewell'), function(){
			frappe.new_doc('Borewell',{'je_name':frm.doc.je_incharge_name,'je_mobile_no':frm.doc.je_contact_no,'block':frm.doc.block,'village':frm.doc.village,'land_type':frm.doc.land_owner_type,'land_identification':frm.doc.name})
			// frappe.msgprint('Hello')
		}); 
	}

	}
});
