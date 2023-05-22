CREATE TEMPORARY [STREAMING] LIVE VIEW view_name
  [(
    [
    col_name1 [ COMMENT col_comment1 ],
    col_name2 [ COMMENT col_comment2 ],
    ...
    ]
    [
    CONSTRAINT expectation_name_1 EXPECT (expectation_expr1) [ON VIOLATION { FAIL UPDATE | DROP ROW }],
    CONSTRAINT expectation_name_2 EXPECT (expectation_expr2) [ON VIOLATION { FAIL UPDATE | DROP ROW }],
    ...
    ]
  )]
  [COMMENT view_comment]
  AS select_statement