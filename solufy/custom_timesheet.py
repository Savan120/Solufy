import frappe
from frappe import _
from frappe.model.document import Document

def update_issue_with_actual_time(timesheet_name,issue_name):
    total_actual_hour = 0
    for row in timesheet_name.time_logs:
        total_actual_hour += row.hours
        frappe.db.set_value("Issue Child Table", {"user_name": frappe.session.user, "parent": row.custom_issue }, {"actual_time": total_actual_hour})

