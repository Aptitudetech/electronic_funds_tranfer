# Copyright (c) 2013, CloudGround / Aptitudetech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = [_("Invoice") + "::120", _("Date") + "::140",
                _("Total") + "::120", _("Payment Amount") + "::140", _("Credit") + "::120"]
	conditions = ""
	if filters.get("supplier"):
                conditions += " and efti.supplier = %(supplier)s"

	if filters.get("eft"):
		conditions += " and eft.name = %(eft)s"

	data = get_data(conditions, filters)
	nb_row = len(data)
	x = 0
	total_payment_amount = total_invoice = 0.00

	while x < nb_row:
		total_invoice = float(data[x][2]) + float(total_invoice)
		total_payment_amount = float(data[x][2]) + float(total_payment_amount)
		x += 1
	
	data.insert(int(x),["", "Total", round(total_invoice, 2), round(total_payment_amount, 2)])

	return columns, data

def get_data(conditions, filters):
        time_sheet = frappe.db.sql(""" SELECT efti.bill_no, p.bill_date, p.grand_total, efti.grand_total, efti.credit
                FROM `tabAdvance Automatic Payment Tool` eft
                LEFT JOIN `tabAdvance Automatic Payment Tool Item` efti ON  eft.name = efti.parent
                LEFT JOIN `tabPurchase Invoice` p ON p.name = efti.purchase_invoice
                WHERE 1=1 %s order by efti.supplier """%(conditions), filters, as_list=1)

        return time_sheet
