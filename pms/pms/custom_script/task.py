import frappe
import time
import json
from frappe.model.mapper import get_mapped_doc

def after_insert(doc,method):
    set_block_village_on_task(doc)

def set_block_village_on_task(doc):
    if doc.project:
        proj_template = frappe.db.get_value("Project", {'name':doc.project}, "project_template")
        task_template_list = frappe.db.get_all("Project Template Task", {'parent':proj_template}, ['task', 'subject', 'location','village'])
        task_list = frappe.db.get_all("Task", {'project':doc.project}, ['name', 'subject'])
        if doc.name not in [t.name for t in task_list]:
            task_list.append({'name':doc.name, 'subject':doc.subject})
        if len(task_list) == len(task_template_list):
            subject_list = set([t.get('subject') for t in task_list])
            for sub in subject_list:
                associated_task = [t.get('name') for t in task_list if t.get('subject')==sub]
                associated_task = set(associated_task)
                associated_task = list(associated_task)
                if doc.subject == sub and doc.name not in associated_task:
                    associated_task.append(doc.name)
                loc_villg_data = frappe.db.sql("""Select distinct subject,location,village from
                    `tabProject Template Task`  where parent='{0}' and subject='{1}'""".format(proj_template,sub), as_dict=1)
                for l in loc_villg_data:
                    for a in associated_task:
                        if loc_villg_data.index(l) == associated_task.index(a):
                            l.update({'task':a})
                            frappe.db.sql("""update `tabTask` set location='{0}', village='{1}' 
                                where name='{2}'""".format(l.location, l.village, l.task))

@frappe.whitelist()
def check_task_status(task_list):
    task_list = json.loads(task_list)
    result = False
    for task in task_list:
        status = frappe.db.get_value("Task", {'name':task},'status')
        if status in ["Completed", "Cancelled"]:
            result = True
        else:
            result = False
    return result


@frappe.whitelist()
def make_material_request(source_name, target_doc=None):
    def set_missing_values(source,target):
        for item in source.task_item:
            mr_row = target.append('items', {})
            mr_row.item_code = item.item_code
            mr_row.item_name = item.item_name
            mr_row.qty = item.qty
            mr_row.project = source.project
            mr_row.description = item.description
            mr_row.uom = item.uom
            mr_row.stock_uom = frappe.db.get_value("Item", {'name':item.item_code}, 'stock_uom')
    return get_mapped_doc("Task", source_name, {
        "Task": {
            "doctype": "Material Request",
            "field_map": {
                "name": 'task'
            },
        }
    }, target_doc,set_missing_values)