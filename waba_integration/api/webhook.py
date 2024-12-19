import frappe
from waba_integration.whatsapp_business_api_integration.doctype.waba_whatsapp_message.waba_whatsapp_message import (
	create_waba_whatsapp_message,
	process_status_update,
)

from werkzeug.wrappers import Response


@frappe.whitelist(allow_guest=True)
def handle():
	
	if frappe.request.method == "GET":
		return verify_token_and_fulfill_challenge()

	try:
		form_dict = frappe.local.form_dict
		frappe.get_doc(
			{"doctype": "WABA Webhook Log", "payload": frappe.as_json(form_dict)}
		).insert(ignore_permissions=True)

		messages = form_dict["entry"][0]["changes"][0]["value"].get("messages", [])
		statuses = form_dict["entry"][0]["changes"][0]["value"].get("statuses", [])

		for status in statuses:
			process_status_update(status)

		for message in messages:
			# find if a WABA WhatsApp Message with Message ID exists in the system
			# if not, create a new WABA WhatsApp Message
			if not frappe.db.exists("WABA WhatsApp Message", {"id": message.get("id")}):
				create_waba_whatsapp_message(message)

		
	except Exception:
		form_dict = frappe.local.form_dict
		frappe.get_doc(
			{"doctype": "WABA Webhook Log", "payload": frappe.as_json(form_dict)}
		).insert(ignore_permissions=True)
		frappe.log_error("WABA Webhook Log Error", frappe.get_traceback())
		frappe.log_error("Log From IDML", frappe.as_json(form_dict))
		frappe.throw("Something went wrong")


def verify_token_and_fulfill_challenge():
	meta_challenge = frappe.form_dict.get("hub.challenge")
	expected_token = frappe.db.get_single_value("WABA Settings", "webhook_verify_token")

	if frappe.form_dict.get("hub.verify_token") != expected_token:
		frappe.throw("Verify token does not match")

	return Response(meta_challenge, status=200)
