# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Test Subject Tests
# MAGIC
# MAGIC Includes
# MAGIC - test_add
# MAGIC - test_subtract
# MAGIC - test_multiple

# COMMAND ----------

# DBTITLE 1,run testsubject1
# MAGIC %run ./testsubject1

# COMMAND ----------

class Testmodule1(unittest.TestCase):
  
  @classmethod
  def setUpClass(cls):
    cls.calculator_inst = calculator(x = 100, y = 200, spark = spark, dbutils = dbutils)

  def setUp(self):
    print("this is setup for every method")
    print(self.id())
    pass

  def test_add(self):
    self.assertEqual(self.calculator_inst.add(10,5), 15)
    print(f"{self} passed OK")

  def test_subtract(self):
    self.assertEqual(self.calculator_inst.subtract(10,5), 5)
    self.assertNotEqual(self.calculator_inst.subtract(10,2), 4)

  def test_multiply(self):
    self.assertEqual(self.calculator_inst.multiply(10,5), 50)

  def test_boolean(self):
    self.assertTrue(True) # Passes if result is True
    self.assertFalse(error)  # Passes if error is False

    # 4. assertIs(a, b): Checks if a is the same object as b.

    # self.assertIs(result, expected_result)  # Passes if result is expected_result (same object)

    # 5. assertIsNone(x): Checks if x is None.

    # self.assertIsNone(result)  # Passes if result is None

    # 6. assertIsNotNone(x): Checks if x is not None.

    # self.assertIsNotNone(result)  # Passes if result is not None

    # 7. assertIn(a, b): Checks if a is present in b.

    # self.assertIn(item, my_list)  # Passes if item is present in my_list

    # 8. assertNotIn(a, b): Checks if a is not present in b.

    # self.assertNotIn(item, my_list)  # Passes if item is not present in my_list

    # 9. assertRaises(exception, callable, *args, **kwargs): Checks if calling callable raises exception.

    # self.assertRaises(ValueError, divide, 10, 0)  # Passes if calling divide(10, 0) raises ValueError

    # 10. assertAlmostEqual(a, b, places): Checks if a and b are approximately equal up to a specified number of decimal places.

    # self.assertAlmostEqual(result, expected_result, places=2)  # Passes if result and expected_result are approximately equal up to 2 decimal places



  def tearDown(self):
    print("teardown for every method")
    pass

  @classmethod
  def tearDownClass(cls):
    print("this is teardown class")
    pass
    


# COMMAND ----------

# class NotebookTests(unittest.TestCase):
  
# #   @classmethod
# #   def setUpClass(cls):
# #     cls.calculator_inst = calculator(x = 100, y = 200, spark = spark, dbutils = dbutils)

#   def setUp(self):
#     print("this is setup for every method")
#     print(self.id())
#     pass

#   def test_add(self):
#     self.assertEqual(self.calculator_inst.add(10,5), 15, )
#     print(f"{self} passed OK")

#   def test_subtract(self):
#     self.assertEqual(self.calculator_inst.subtract(10,5), 5)
#     self.assertNotEqual(self.calculator_inst.subtract(10,2), 4)

#   def test_multiply(self):
#     self.assertEqual(self.calculator_inst.multiply(10,5), 50)

#   def tearDown(self):
#     print("teardown for every method")
#     pass

#   @classmethod
#   def tearDownClass(cls):
#     print("this is teardown class")
#     pass