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
                        "label": __("EFT"),
                        "fieldtype": "Link",
                        "options": "Electronic Funds Transfer",
                        "default": ""
                },

	]
}
