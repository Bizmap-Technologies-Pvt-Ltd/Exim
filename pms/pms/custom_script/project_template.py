import frappe

def validate(doc,method):
    set_block_village_on_task(doc)

def set_block_village_on_task(doc):
    for t in doc.tasks:
        if t.task and t.location and t.village:
            task_doc = frappe.get_doc("Task",t.task )
            print("t.task",task_doc.name,"@@@@@@ task_doc.location",task_doc.location, "task_doc.village",task_doc.village)
            if task_doc.location == None and task_doc.village == None:

                print("#### if task_doc.location",task_doc.location,"task_doc.village",task_doc.village)
            #     continue
            # else:
            print("else t.location",t.location, "t.village",t.village)
            task_doc.location = t.location 
            task_doc.village = t.village 
            task_doc.save()

            # frappe.db.sql(f"""update `tabTask` set location = '{t.location}' 
            #   and village= '{t.village}' where name = '{t.task}'""")
            # frappe.db.commit()
