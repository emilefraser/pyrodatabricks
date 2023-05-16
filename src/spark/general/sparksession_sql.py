result_df = spark.sql("""
SELECT name, price
FROM products
WHERE price < 200
ORDER BY price
""")

display(result_df)