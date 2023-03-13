-- Recursively vacuum directories associated with the Delta table. VACUUM removes all files from the table directory that are not managed by Delta, 
-- as well as data files that are no longer in the latest state of the transaction log for the table and are older than 
-- a retention threshold

-- 0 HOURS RETENTION = keep no history

-- To run with 0 hour retention you have to
-- Turn off a check to prevent premature deletion of data files
-- Make sure that logging of VACUUM commands is enabled
-- Use the DRY RUN version of vacuum to print out all records to be deleted

VACUUM table_name [RETAIN num HOURS] [DRY RUN]