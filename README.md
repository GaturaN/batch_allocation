## Allocate Batch

Creates batches for items with transaction but have no batches in the system. It does not allocate the existing stock to the batch. This can be done through Stock Reconciliation or modify the code to allocate existing stock to the created batch.

## Handling Patch Execution Issues

If the patch does not run during site migrate, it might be because the app has been installed with the patch logs already recorded. To resolve this, follow the steps below:

1. **Access MariaDB and Search for Patch Logs:**

    Use the following command to search for the relevant patch logs:
    
    ```sql
    SELECT * FROM tabPatch Log WHERE name LIKE '%allocate_batch%';
    ```

2. **Delete the Patch Logs:**

    To delete the logs, use the command below:
    
    ```sql
    DELETE FROM tabPatch Log WHERE name LIKE '%allocate_batch%';
    ```

    If you encounter an error, try the alternative commands:

    ```sql
    SET SQL_SAFE_UPDATES = 0;
    DELETE FROM tabPatch Log WHERE patch LIKE '%allocate_batch%';
    SET SQL_SAFE_UPDATES = 1;
    ```

3. **Run the Patch Again:**

    Once the logs are deleted, you can run the patch again using the following command:

    ```bash
    bench --site site.name run-patch allocate_batch.patches.batch_prod
    ```


#### License

MIT