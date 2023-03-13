row = spark.table("beans").filter("name='pinto'").first()
assert row["color"] == "brown", "The pinto bean should be labeled as the color brown"
assert row["grams"] == 1500, "Make sure you correctly specified the `grams` as 1500"
assert row["delicious"] == True, "The pinto bean is a delicious bean"