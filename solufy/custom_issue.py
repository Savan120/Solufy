import frappe
from frappe import _
from datetime import datetime

def validate_issue_time_involvement(doc, method):
    total_time_involvement = 0
    total_actual_hrs = 0

    existing_entry = None
    for row in doc.get("custom_time_involvement_table"):
        if row.user_name == frappe.session.user:
            existing_entry = row
            break

    if len(doc.custom_time_involvement_table) < 1:
        if not existing_entry and doc.custom_assigned_to:
            doc.append("custom_time_involvement_table", {
                "user_name": frappe.session.user,
                "full_name": frappe.utils.get_fullname(frappe.session.user),
                "time_involvement": 0.25,
                "actual_time": 0,
                "date": datetime.now().strftime('%Y-%m-%d')
            })

    for row in doc.get("custom_time_involvement_table"):
        total_time_involvement += row.time_involvement or 0
        total_actual_hrs += row.actual_time or 0

    doc.custom_time_involvement = total_time_involvement
    doc.custom_actual_hrs = total_actual_hrs


def calculate_custom_actual_hours(doc, method):
    total_actual_hours = 0
    if doc.custom_time_involvement_table:
        total_actual_hours = sum([row.actual_time or 0 for row in doc.custom_time_involvement_table])
    
    doc.custom_actual_hrs = total_actual_hours