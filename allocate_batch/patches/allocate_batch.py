import frappe

def execute():
    print("Patch is running")
    
    # Get all items with transactions and no batches
    items = frappe.db.sql("""
        SELECT DISTINCT item.item_code
        FROM `tabItem` item
        JOIN `tabStock Ledger Entry` sle ON item.item_code = sle.item_code
        LEFT JOIN `tabBatch` batch ON item.item_code = batch.item
        WHERE batch.name IS NULL
        GROUP BY item.item_code
    """, as_dict=True)
    
    for item in items:
        item_code = item['item_code']
        batch_name = f"{item_code}-00001"

        # Check if the batch already exists
        if not frappe.db.exists('Batch', batch_name):
            # Create a new batch if it doesn't exist
            batch = frappe.get_doc({
                'doctype': 'Batch',
                'batch_id': batch_name,
                'item': item_code,
                'item_code': item_code
            })
            try:
                batch.insert(ignore_permissions=True)
                frappe.db.commit()
                print(f"Created default batch: {batch_name} for item: {item_code}")
            except Exception as e:
                print(f"Error creating batch for item {item_code}: {str(e)}")
        
        # Enable batch tracking for the item
        if not frappe.db.get_value('Item', item_code, 'has_batch_no'):
            item_doc = frappe.get_doc('Item', item_code)
            item_doc.has_batch_no = 1
            try:
                item_doc.save(ignore_permissions=True)
                frappe.db.commit()
                print(f"Enabled batch tracking for item: {item_code}")
            except Exception as e:
                print(f"Error updating item {item_code}: {str(e)}")