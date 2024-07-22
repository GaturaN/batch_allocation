import frappe

def execute():
    # Print a message indicating that the patch script has started running
    print("Patch is running")
    
    # SQL query to get all unique item codes that have transactions but no associated batches
    items = frappe.db.sql("""
        SELECT DISTINCT item.item_code
        FROM `tabItem` item
        JOIN `tabStock Ledger Entry` sle ON item.item_code = sle.item_code
        LEFT JOIN `tabBatch` batch ON item.item_code = batch.item
        WHERE batch.name IS NULL
        GROUP BY item.item_code
    """, as_dict=True) #as_dict ensures query is returned as list of dictionaries rather than a list of tuples
    
    # Iterate over each item obtained from the query
    for item in items:
        item_code = item['item_code']  # Extract the item code from the current item
        batch_name = f"{item_code}-00001"  # Default batch name series

        # Check if a batch with the default batch name already exists
        if not frappe.db.exists('Batch', batch_name):
            # If the batch does not exist, create a new batch
            batch = frappe.get_doc({
                'doctype': 'Batch',  # Specify the doctype as 'Batch'
                'batch_id': batch_name,  # Set the batch ID to the default batch name
                'item': item_code,  # Associate the batch with the item code
                'item_code': item_code  # Redundant field to associate the batch with the item code
            })
            try:
                # Insert the new batch into the database, ignoring permissions
                batch.insert(ignore_permissions=True)
                # Commit the transaction to save the changes
                frappe.db.commit()
                # Print a success message indicating the batch was created
                print(f"Created default batch: {batch_name} for item: {item_code}")
            except Exception as e:
                # Print an error message if batch creation fails
                print(f"Error creating batch for item {item_code}: {str(e)}")
                frappe.db.rollback()
        
        # # Check if batch tracking is enabled for the item
        # if not frappe.db.get_value('Item', item_code, 'has_batch_no'):
        #     # If not, retrieve the item document
        #     item_doc = frappe.get_doc('Item', item_code)
        #     # Enable batch tracking by setting the has_batch_no field to 1
        #     item_doc.has_batch_no = 1
        #     try:
        #         # Save the updated item document, ignoring permissions
        #         item_doc.save(ignore_permissions=True)
        #         # Commit the transaction to save the changes
        #         frappe.db.commit()
        #         # Print a success message indicating batch tracking was enabled
        #         print(f"Enabled batch tracking for item: {item_code}")
        #     except Exception as e:
        #         # Print an error message if enabling batch tracking fails
        #         print(f"Error updating item {item_code}: {str(e)}")