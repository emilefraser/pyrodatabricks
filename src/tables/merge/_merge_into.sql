--  Merges a set of updates, insertions, and deletions based on a source table into a target Delta table.

--This statement is supported only for Delta Lake tables.

-- Therefore, this action assumes that the source table has the same columns as those in the target table, 
--      otherwise the query will throw an analysis error. This behavior changes when automatic schema migration is enabled


MERGE INTO target_table_name [target_alias]
   USING source_table_reference [source_alias]
   ON merge_condition
   { WHEN MATCHED [ AND matched_condition ] THEN matched_action |
     WHEN NOT MATCHED [BY TARGET] [ AND not_matched_condition ] THEN not_matched_action |
     WHEN NOT MATCHED BY SOURCE [ AND not_matched_by_source_condition ] THEN not_matched_by_source_action } [...]

matched_action
 { DELETE |
   UPDATE SET * |
   UPDATE SET { column = { expr | DEFAULT } } [, ...] }

not_matched_action
 { INSERT * |
   INSERT (column1 [, ...] ) VALUES ( expr | DEFAULT ] [, ...] )

not_matched_by_source_action
 { DELETE |
   UPDATE SET { column = { expr | DEFAULT } } [, ...] }