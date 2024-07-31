import frappe


def execute():
    """
    This function executes the patch script to create default batches for items that have transactions but no associated batches.
    It retrieves distinct item codes from the 'Item' and 'Stock Ledger Entry' tables and checks if each item has an associated batch.
    If an associated batch does not exist, it creates a new batch with the default batch name format of "{item_code}-00001".
    """

    # Retrieve distinct item codes from the 'Item' and 'Stock Ledger Entry' tables
    items = frappe.db.sql(
        """
        SELECT DISTINCT item.item_code
        FROM `tabItem` item
        JOIN `tabStock Ledger Entry` sle ON item.item_code = sle.item_code
        LEFT JOIN `tabBatch` batch ON item.item_code = batch.item
        WHERE batch.name IS NULL
        GROUP BY item.item_code
        """,
        as_dict=True
    )

    # Iterate over each item code
    for item in items:
        item_code = item["item_code"]
        default_batch_name = f"{item_code}-00001"
        
        # update fields in item
        frappe.db.set_value("Item", item_code, {
            "has_batch_no":1,
            "create_new_batch":1,
            "batch_number_series":item_code,
            "has_expiry_date":1
         })
        frappe.db.commit()
        
        
        
        # Check if a batch with the default batch name already exists
        if not frappe.db.exists("Batch", default_batch_name):
            # Create a new batch if it does not exist
            batch = frappe.get_doc(
                {
                    "doctype": "Batch",
                    "batch_id": default_batch_name,
                    "item": item_code,
                    "item_code": item_code
                }
            )
            try:
                # Insert the new batch into the database
                batch.insert(ignore_permissions=True)
                frappe.db.commit()
            except Exception as e:
                # Rollback the transaction if an error occurs
                frappe.db.rollback()
