# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "electronic_funds_transfer"
app_title = "Electronic Funds Transfer"
app_publisher = "CloudGround / Aptitudetech"
app_description = " Electronic Funds Transfer (EFT) Direct Deposit is an electronic payment service that provides your business with a fast and simple way to issue Canadian and U.S. dollar payments to accounts at any financial institution in Canada."
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "support@cloudground.ca"
app_license = "GNU V3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/electronic_funds_transfer/css/electronic_funds_transfer.css"
# app_include_js = "/assets/electronic_funds_transfer/js/electronic_funds_transfer.js"

# include js, css files in header of web template
# web_include_css = "/assets/electronic_funds_transfer/css/electronic_funds_transfer.css"
# web_include_js = "/assets/electronic_funds_transfer/js/electronic_funds_transfer.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "electronic_funds_transfer.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "electronic_funds_transfer.install.before_install"
# after_install = "electronic_funds_transfer.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "electronic_funds_transfer.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"electronic_funds_transfer.tasks.all"
# 	],
# 	"daily": [
# 		"electronic_funds_transfer.tasks.daily"
# 	],
# 	"hourly": [
# 		"electronic_funds_transfer.tasks.hourly"
# 	],
# 	"weekly": [
# 		"electronic_funds_transfer.tasks.weekly"
# 	]
# 	"monthly": [
# 		"electronic_funds_transfer.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "electronic_funds_transfer.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "electronic_funds_transfer.event.get_events"
# }

