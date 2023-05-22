CREATE OR REFRESH [TEMPORARY] { STREAMING TABLE | LIVE TABLE } table_name
  [(
    [
    col_name1 col_type1 [ GENERATED ALWAYS AS generation_expression1 ] [ COMMENT col_comment1 ],
    col_name2 col_type2 [ GENERATED ALWAYS AS generation_expression2 ] [ COMMENT col_comment2 ],
    ...
    ]
    [
    CONSTRAINT expectation_name_1 EXPECT (expectation_expr1) [ON VIOLATION { FAIL UPDATE | DROP ROW }],
    CONSTRAINT expectation_name_2 EXPECT (expectation_expr2) [ON VIOLATION { FAIL UPDATE | DROP ROW }],
    ...
    ]
  )]
  [USING DELTA]
  [PARTITIONED BY (col_name1, col_name2, ... )]
  [LOCATION path]
  [COMMENT table_comment]
  [TBLPROPERTIES (key1 [ = ] val1, key2 [ = ] val2, ... )]
  AS select_statement