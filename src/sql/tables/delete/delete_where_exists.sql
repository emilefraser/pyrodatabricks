DELETE FROM orders AS t1
   WHERE EXISTS (SELECT oid FROM returned_orders WHERE t1.oid = oid)