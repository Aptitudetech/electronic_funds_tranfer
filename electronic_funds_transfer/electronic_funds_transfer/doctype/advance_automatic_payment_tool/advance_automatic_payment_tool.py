# -*- coding: utf-8 -*-
# Copyright (c) 2017, CloudGround / Aptitudetech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
import unicodedata
from frappe import _
from frappe.model.document import Document
from frappe.utils.file_manager import save_file
from frappe import utils
from erpnext.accounts.doctype.journal_entry.journal_entry import get_payment_entry_against_invoice
from erpnext.accounts.doctype.payment_request.payment_request import make_payment_entry
from erpnext.accounts.doctype.payment_entry.payment_entry import get_party_details
from erpnext.accounts.doctype.payment_entry.payment_entry import get_account_details
from erpnext.accounts.doctype.payment_entry.payment_entry import get_reference_details
#from frappe.contacts.doctype.address.address import get_default_address

class AdvanceAutomaticPaymentTool(Document):
	def validate(self):
                self.total_amount()
    
	def on_submit(self):
		bank_detail = frappe.get_doc("Electronic Funds Transfer Bank Detail", self.bank_account)
		frappe.db.set(self, 'file_creation_number', bank_detail.file_creation_number.zfill(4))
		frappe.db.set(self, 'transfert_date', self.posting_date)

		bank_detail.file_creation_number = str(int(bank_detail.file_creation_number) + 1)
		bank_detail.save()
		
	def total_amount(self):
		total = 0.0
		for d in self.get('items_eft'):
			total += d.grand_total
		for d in self.get('items_cheque'):
			total += d.grand_total
		self.total_transfer = total

	def download_test(self):
		str_save_file = "A"
		str_save_file += frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "originator_id").zfill(10)
		str_save_file += self.file_creation_number.zfill(4)

		today = datetime.date.today()

		str_save_file += "0" + today.strftime("%y%j")
		str_save_file += frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "destination_data_centre_code").zfill(5)

		str_save_file += "\nXC430"
		str_save_file += "0" + today.strftime("%y%j")
		str_save_file += frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "originators_short").ljust(15)
		str_save_file += frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "originators_long").ljust(30)
		str_save_file += "0"
		str_save_file += frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "institution_number").ljust(3)
		str_save_file += frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "branch_number").ljust(5)
		str_save_file += frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "account_number").ljust(12)

		count = 0
		total = 0.00

		for supplier, dict_invoice in self.create_dict_from_list(self.get('items_eft')).items():
			grand_total = 0.00
			for invoice_name, grand_total_invoice in dict_invoice.items():
				grand_total = grand_total + grand_total_invoice
			str_save_file += "\nC"
			str_save_file += "{:.2f}".format(grand_total).replace('.','').replace(',','').zfill(10)
			str_save_file += "0"
			str_save_file += frappe.db.get_value("Electronic Funds Transfer Supplier Information", {'supplier':supplier}, "institution_number").zfill(3)
			str_save_file += frappe.db.get_value("Electronic Funds Transfer Supplier Information", {'supplier':supplier}, "branch_number").zfill(5)
			str_save_file += frappe.db.get_value("Electronic Funds Transfer Supplier Information", {'supplier':supplier}, "account_number").ljust(12)
			supplier_without_accent = ''.join((c for c in unicodedata.normalize('NFD', supplier) if unicodedata.category(c) != 'Mn'))
			#supplier_without_accent = supplier
			str_save_file += supplier_without_accent.ljust(29)[:29]
			str_save_file += supplier_without_accent.ljust(19)[:19]
			count += 1
			total += grand_total

		str_save_file += "\nYC" + str(count).zfill(8) + "{:.2f}".format(total).replace('.','').replace(',','').zfill(14)
		var_zero = 0
		str_save_file += "\nZ" + str(var_zero).zfill(14) + str(var_zero).zfill(5) +  "{:.2f}".format(total).replace('.','').replace(',','').zfill(14) + str(count).zfill(5)

		save_file("file-bank-transfer.txt", str_save_file, self.doctype, self.name, is_private=True)
		frappe.db.set(self, 'is_file_generated', True)

	def import_overdue_purchase_invoice(self):
		self.items_eft = []
		self.items_cheque = []
		currency = "CAD"
		if self.sort_by == "Supplier Name":
			order = "supplier"
		elif self.sort_by == "Due Date (oldest first)":
			order = "due_date"
		if self.supplier_filter:
			lst_pi = frappe.get_list("Purchase Invoice", fields=["name"], filters={"due_date": ("<=", self.posting_date), "outstanding_amount": ("!=", 0), "status": ("!=", "Paid"), "docstatus": 1, "supplier": self.supplier_filter, "currency": currency})
		else:
			lst_pi = frappe.get_list("Purchase Invoice", fields=["name"], filters={"due_date": ("<=", self.posting_date), "outstanding_amount": ("!=", 0), "status": ("!=", "Paid"), "docstatus": 1, "currency": currency}, order_by=order)
		
		for pi in lst_pi:
			credit = 0
			lst_cr = frappe.get_list("Purchase Invoice", fields=["name", "grand_total"], filters={"return_against": ("=", pi.name), "status": ("!=", "Paid"), "docstatus": 1})
			for cr in lst_cr:
				credit = cr.grand_total
#				if credit != 0:
#					frappe.msgprint(str(credit))
                        pi = frappe.get_doc("Purchase Invoice", pi.name)
			if pi.bill_date:
				aging = frappe.utils.date_diff(self.posting_date, pi.bill_date)
			else:
				aging = frappe.utils.date_diff(self.posting_date, pi.posting_date)
			b = False
			if frappe.db.exists("Electronic Funds Transfer Supplier Information", pi.supplier):	
				for i in self.get('items_eft'):
					if i.purchase_invoice == pi.name:
						b = True
				if b == False :
					self.append("items_eft",
					{
						"purchase_invoice": pi.name,
						"supplier": pi.supplier,
						"grand_total": pi.outstanding_amount,
						"bill_no": pi.bill_no,
						"credit": credit,
						"aging": aging 
					})
			else:
				for i in self.get('items_cheque'):
					if i.purchase_invoice == pi.name:
						b = True
				if b == False :
					self.append("items_cheque",
					{
						"purchase_invoice": pi.name,
						"supplier": pi.supplier,
						"grand_total": pi.outstanding_amount,
						"bill_no": pi.bill_no,
						"credit": credit,
						"aging": aging
					})
		self.total_amount()
		#self.save()
	def create_dict_from_list(self, list1):
		dict1  = {
            "supplier" : {"invoice_no" : 100.01}
        }
		dict1.clear()
		for d in list1:
			if d.supplier in dict1 :
				dict1[d.supplier][d.purchase_invoice] = d.grand_total
			else:
				dict1[d.supplier] = {}
				dict1[d.supplier][d.purchase_invoice] = d.grand_total
		return dict1
	
	def create_journal_entry(self):
		self.create_payment_entry_list(self.get('items_eft'), "Bank Transfer - CDN")
		self.create_payment_entry_list(self.get("items_cheque"), "Cheque CDN")
		frappe.msgprint("Payment Entry are created.")

	def create_payment_entry_list(self, list1, mode_of_payment):
		for supplier, dict_invoice in self.create_dict_from_list(list1).items():
			cheque_series = 0
			if mode_of_payment == "Cheque CDN" or mode_of_payment == "Cheque USD":
				cheque_series = frappe.db.get_value("Cheque Series", self.bank_account, "cheque_series")
				cheque_series = int(cheque_series) + 1

			if mode_of_payment != "Cheque CDN" and mode_of_payment != "Cheque USD":
				cheque_series = self.file_creation_number

			pme = frappe.new_doc("Payment Entry")
			paid_from_account_name = frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "account")
			company_name = frappe.db.get_value("Account", paid_from_account_name, "company")
			posting_date_today = utils.today()
			posting_date_today = utils.getdate(self.posting_date)
			party_details = get_party_details(company_name, "Supplier", supplier, posting_date_today)
			paid_from_account_detail = get_account_details(paid_from_account_name, posting_date_today)
			paid_to_account_detail = get_account_details(party_details["party_account"], posting_date_today)
			json_update = {
					"naming_series": "PE-",
					"payment_type": "Pay",
					"party_type": "Supplier",
					"party": supplier,
					"posting_date": datetime.date.today(),
					"company" : company_name,
					"mode_of_payment": mode_of_payment,
					"paid_from": paid_from_account_name,
					"paid_from_account_currency": party_details["party_account_currency"],
					"party_balance": party_details["party_balance"],
					"paid_to" : party_details["party_account"],
					"paid_to_account_currency": paid_to_account_detail["account_currency"],
					"paid_to_account_balance" : paid_to_account_detail["account_balance"],
					"reference_no" : cheque_series,
					"reference_date" : posting_date_today,
			}
			pme.update (json_update)
			received_amount = 0.00
			#frappe.msgprint(str(json_update))
			for invoice_name, grand_total in dict_invoice.items():
				#frappe.msgprint(str(invoice_name))
				if grand_total > 0:
					received_amount = received_amount + grand_total
					reference_detail = get_reference_details("Purchase Invoice", invoice_name, party_details["party_account_currency"])
					if reference_detail["exchange_rate"] != 1:
						frappe.throw(_("We don't support multi currency yet.  Please check invoice # " + invoice_name + " for supplier : " + supplier));

					if grand_total != reference_detail["outstanding_amount"] :
						frappe.throw(_("The outstanding amount as change since the creation of the AAPT purchase_invoice : " + invoice_name + " for supplier : " + supplier));

					pme.append("references", {
						"reference_doctype": "Purchase Invoice",
						"reference_name": invoice_name,
						"due_date": reference_detail["due_date"],
						"total_amount": reference_detail["total_amount"],
						"outstanding_amount": reference_detail["outstanding_amount"],
						"allocated_amount": grand_total,
						"exchange_rate": reference_detail["exchange_rate"]
					})
					#frappe.msgprint(str({
                                        #        "reference_doctype": "Purchase Invoice",
                                        #        "reference_name": invoice_name,
                                        #        "due_date": reference_detail["due_date"],
                                        #        "total_amount": reference_detail["total_amount"],
                                        #        "outstanding_amount": reference_detail["outstanding_amount"],
                                        #        "allocated_amount": grand_total,
                                        #        "exchange_rate": reference_detail["exchange_rate"]
                                        #}))
				else:
					pi = frappe.get_doc("Purchase Invoice", {"return_against": invoice_name})
					reference_detail = get_reference_details("Purchase Invoice", pi.return_against, party_details["party_account_currency"])
					if grand_total != reference_detail["outstanding_amount"] :
                                                frappe.throw(_("The outstanding amount as change since the creation of the AAPT purchase_invoice : " + invoice_name + " for supplier : " + supplier));
					if reference_detail["exchange_rate"] != 1:
                                                frappe.throw(_("We don't support multi currency yet.  Please check invoice # " + invoice_name + " for supplier : " + supplier));

					if reference_detail["outstanding_amount"] < 0:
						pmer = frappe.new_doc("Payment Entry")
						json_update = {
							"naming_series": "PE-",
							"payment_type": "Receive",
							"party_type": "Supplier",
							"party": supplier,
							"posting_date": datetime.date.today(),
							"company" : company_name,
							"mode_of_payment": mode_of_payment,
							"paid_from": party_details["party_account"],
							"paid_from_account_currency": paid_to_account_detail["account_currency"],
							"party_balance": party_details["party_balance"],
							"paid_to" : paid_from_account_name,
							"paid_to_account_currency": party_details["party_account_currency"],
							"paid_to_account_balance" : paid_to_account_detail["account_balance"],
							"reference_no" : cheque_series,
							"reference_date" : posting_date_today,
						}
						pmer.update (json_update)
						#frappe.msgprint("total_amount" + str(reference_detail["total_amount"]))
                                        	#frappe.msgprint("allocated_amount" + str(reference_detail["outstanding_amount"]))
                                        	#frappe.msgprint("allocated_amount" + str(grand_total))
						pmer.append("references", {
							"reference_doctype": "Purchase Invoice",
							"reference_name": pi.name,
							"due_date": reference_detail["due_date"],
							"total_amount": reference_detail["total_amount"],
							"outstanding_amount": reference_detail["outstanding_amount"],
							"allocated_amount": grand_total,
							"exchange_rate": reference_detail["exchange_rate"]
						})
						#frappe.msgprint(str(0-grand_total))
						pmer.received_amount = 0-grand_total
						pmer.paid_amount = 0-grand_total
						pmer.save()
						pmer.submit()
						#frappe.msgprint("Submit Retour")
			pme.received_amount = received_amount
			pme.paid_amount = received_amount
			#frappe.msgprint(str(received_amount))
			if received_amount != 0:
				pme.save()
				pme.submit()
			if mode_of_payment == "Cheque CDN" or mode_of_payment == "Cheque USD":
				frappe.client.set_value("Cheque Series", self.bank_account, "cheque_series", cheque_series)
		#frappe.msgprint("Payment Entry are created.")
		frappe.db.set(self, 'is_payment_entry_generated', True)
	
	def get_default_address(doctype, name, sort_key='is_primary_address'):
		'''Returns default Address name for the given doctype, name'''
		out = frappe.db.sql('''select parent,
						(select `{0}` from tabAddress a where a.name=dl.parent) as `{0}`
					from
						`tabDynamic Link` dl
					where
						link_doctype=%s and
						link_name=%s and
						parenttype = "Address"
				'''.format(sort_key), (doctype, name))

		if out:
				return sorted(out, lambda x,y: cmp(y[1], x[1]))[0][0]
		else:
				return None

	def send_email_notification(self):
		ae = frappe.get_doc("Auto Email Report", "Electronic Fund Transfert Notification - Notification de transfert de fonds electronique")
		no_error = True		
		
		#frappe.msgprint("debut loop item_eft")
		for supplier, dict_invoice in self.create_dict_from_list(self.get('items_eft')).items():
			#Get default billing email
			lst_dl = frappe.get_list("Dynamic Link", fields=["parent"], filters={"link_doctype": "supplier", "link_name": supplier})
			default_email = ""
			for dl in lst_dl:
				if frappe.db.exists('Address', dl.parent):
					address = frappe.get_doc('Address', dl.parent)
                	        	if address.is_primary_address == True:
                	       	        	if address.email_id:
							a=1
						else:
							no_error = False
							frappe.msgprint("Supplier : " + supplier  + ".  Don't have defaut email.")
		if no_error == True:
			for supplier, dict_invoice in self.create_dict_from_list(self.get('items_eft')).items():
				#Get default billing email
				lst_dl = frappe.get_list("Dynamic Link", fields=["parent"], filters={"link_doctype": "supplier", "link_name": supplier})
				default_email = ""
				for dl in lst_dl:
					if frappe.db.exists('Address', dl.parent):
						address = frappe.get_doc('Address', dl.parent)
						if address.is_primary_address == True:
							default_email = address.email_id
				
				if default_email != "":
					ae.email_to = default_email
					ae.email_to += "\n" + frappe.db.get_value("Electronic Funds Transfer Bank Detail", self.bank_account, "verifying_email")

					ae.filters = '{"supplier":"' + supplier + '","eft":"' + self.name + '"}'
					ae.save()
					ae.check_permission()
					ae.send()
				#frappe.msgprint(str(ae.filters))
			frappe.db.set(self, 'is_email_sent', True)
