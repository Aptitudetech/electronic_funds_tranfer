// Copyright (c) 2017, CloudGround / Aptitudetech and contributors
// For license information, please see license.txt

frappe.ui.form.on('Advance Automatic Payment Tool', {
	refresh: function(frm) {

	}
});

frappe.ui.form.on("Advance Automatic Payment Tool", "refresh", function(frm) {
    if(frm.doc.docstatus == 1){
        frm.add_custom_button(__("Generate Transfer Bank File"), function() {
            // When this button is clicked, do this
                frm.call({
                        'method': 'download_test',
                        'doc': frm.doc,
                        'args': {},

                        callback: function() {
                                cur_frm.reload_doc();
                        }
                });
            });
        }
    });



frappe.ui.form.on("Advance Automatic Payment Tool", "refresh", function(frm) {
    if(frm.doc.docstatus == 1 && frm.doc.is_payment_entry_generated == false){
        frm.add_custom_button(__("Make Payment Entry"), function() {
            // When this button is clicked, do this
                frm.call({
                        'method': 'create_journal_entry',
                        'doc': frm.doc,
                        'args': {},

                        callback: function() {
                                //frappe.set_route("List", "Payment Entry");
                        }
                });
            });
        }
    });

frappe.ui.form.on("Advance Automatic Payment Tool", "refresh", function(frm) {
    if(frm.doc.docstatus == 1){
        frm.add_custom_button(__("Send Email Notification"), function() {
            // When this button is clicked, do this
                frm.call({
                        'method': 'send_email_notification',
                        'doc': frm.doc,
                        'args': {},

                        callback: function() {
                                //frappe.set_route("List", "Payment Entry");
                        }
                });
            });
        }
    });


frappe.ui.form.on("Advance Automatic Payment Tool", "refresh", function(frm) {
    if(frm.doc.docstatus == 0){
        frm.add_custom_button(__("Import Overdue Purchase Invoice"), function() {
            // When this button is clicked, do this
                frm.call({
                        'method': 'import_overdue_purchase_invoice',
                        'doc': frm.doc,
                        'args': {},

                        callback: function() {
                                frm.refresh()
                        }
                });
            });
        }
    });



frappe.ui.form.on("Advance Automatic Payment Tool", "purchase_invoice",
    function(frm, cdt, cdn) {
        frappe.call({
            "method": "frappe.client.get_value",
            args: {
                doctype: "Purchase Invoice",
                fieldname: ["supplier", "grand_total", "bill_no"],
                filters: {name: locals[cdt][cdn].purchase_invoice}
            },
            callback: function (data) {
                Object.keys(data.message).forEach(function(field){
                        frappe.model.set_value(cdt, cdn, field, data.message[field]);
                });
            }
        })
    });

frappe.ui.form.on("Advance Automatic Payment Tool Item", "grand_total", function(frm, cdt, cdn){
    frm.call({
        'method': 'total_amount',
        'doc': frm.doc,
        'args': {}
    });
});

