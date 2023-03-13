-- Optimizes the layout of Delta Lake data. 
--  Optionally optimize a subset of data or colocate data by column. If you do not specify colocation, bin-packing optimization
--  is performed.

-- Bin-packing optimization is idempotent, meaning that if it is run twice on the same dataset, the second run has no effect. It aims to produce evenly-balanced data files with respect to their size on disk, but not necessarily number of tuples per file.

-- Z-Ordering is not idempotent but aims to be an incremental operation. The time it takes for Z-Ordering is not guaranteed to reduce over multiple runs. However, if no new data was added to a partition that was just Z-Ordered, another Z-Ordering of that partition will not have any effect. It aims to produce evenly-balanced data files with respect to the number of tuples, but not necessarily data size on disk. 

OPTIMIZE table_name [WHERE predicate]
  [ZORDER BY (col_name1 [, ...] ) ]