frappe.query_reports["Land Register"] = {
	"filters": [
        {
			fieldname: "block",
			label: __("Block"),
			fieldtype: "Link",
            options: "Location",
			reqd: 1
		},
		
    ]
}