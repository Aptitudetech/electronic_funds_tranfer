// Copyright (c) 2016, CloudGround / Aptitudetech and contributors
// For license information, please see license.txt

frappe.query_reports["EFT for Email"] = {
	"filters": [
		{
                        "fieldname":"supplier",
                        "label": __("Supplier"),
                        "fieldtype": "Link",
                        "options": "Supplier",
                        "default": ""
                },
		{
                        "fieldname":"eft",
                        "label": __("AAPT"),
                        "fieldtype": "Link",
                        "options": "Advance Automatic Payment Tool",
                        "default": ""
                },

	]
}
