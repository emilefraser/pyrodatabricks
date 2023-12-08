# Databricks notebook source
# MAGIC %md 
# MAGIC
# MAGIC ## Generalized test runner

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC https://medium.com/constructor-engineering/faster-pyspark-unit-tests-1cb7dfa6bdf6
# MAGIC https://blog.cellenza.com/en/data/pyspark-unit-test-best-practices/
# MAGIC https://stackoverflow.com/questions/2712831/log-unittest-output-to-a-text-file
# MAGIC
# MAGIC https://learn.microsoft.com/en-us/azure/databricks/notebooks/testing

# COMMAND ----------

#%run ../_core/init

# COMMAND ----------

# scoped imports
#imports = {"unittest": [], "xmlrunner": [], "coverage": []}
#import_module(imports)

# COMMAND ----------

import unittest
#import xmlrunner
#import coverage

# COMMAND ----------

# MAGIC %run ./testsubject1_tests

# COMMAND ----------

verbosity = 1

## HOW TO USE SUITES?

# COMMAND ----------

logster.log_message("======================================================================", "INFO", True)
logster.log_message("TEST: Initialized", "INFO", True)
logster.log_message("----------------------------------------------------------------------", "INFO", True)

# COMMAND ----------

cov = coverage.Coverage()
cov.start()

# suite =  unittest.TestLoader(verbosity=2).loadTestsFromTestCase(Testmodule1)      
suite =  unittest.TestLoader(verbosity=verbosity).loadTestsFromTestCase(Testmodule1)
#runner = xmlrunner.XMLTestRunner(output='/dbfs/tests')
#runner.TextTestRunner(verbosity=2).run(suite)
alltests = unittest.TestSuite((suite))
print(alltests)
varout= unittest.TextTestRunner(verbosity = verbosity).run(alltests)
#print(varout)
print(cov)
cov.stop()
cov.save()
cov.html_report(directory='/dbfs/tests/covhtml')
print(cov)

# COMMAND ----------

from pathlib import Path
Path = Path('Path')
SubDeskTop = Path.joinpath(Path, "subdir")

# COMMAND ----------

# ith self.assertLogs('foo', level='INFO') as cm:
#     logging.getLogger('foo').info('first message')
#     logging.getLogger('foo.bar').error('second message')
# self.assertEqual(cm.output, ['INFO:foo:first message',
#                              'ERROR:foo.bar:second message'])

print(dbutils.fs.ls("/"))
dbutils.fs.<command> ("file:/")



# COMMAND ----------

# MAGIC %fs 
# MAGIC ls dbfs:/_custom_location.db/
# MAGIC

# COMMAND ----------

# MAGIC %sh
# MAGIC
# MAGIC ls -la conf

# COMMAND ----------

# MAGIC %load_ext autoreload
# MAGIC %autoreload 2

# COMMAND ----------

# MAGIC   %reload_ext autoreload

# COMMAND ----------

python -m unittest discover -s <directory> -p '*_test.py'

# COMMAND ----------

import unittest
loader = unittest.TestLoader()
start_dir = 'path/to/your/test/files'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)

run_test = unittest.main(argv=[' '], verbosity=1, exit=False)

# assert run_test.result.wasSuccessful(), 'Test failed; see logs above'

# suite1 = unittest.TestLoader().discover('Test1', pattern = "Test*.py")
# suite2 = unittest.TestLoader().discover('Test2', pattern = "Test*.py")
# alltests = unittest.TestSuite((suite1, suite2))
# unittest.TextTestRunner(verbosity=2).run(alltests)



# loader = unittest.TestLoader()
# loader.testMethodPrefix = "test_prefix"# default value is "test"

# suite1 = loader.discover('Test1', pattern = "Test*.py") 
# suite2 = loader.discover('Test2', pattern = "Test*.py")
# alltests = unittest.TestSuite((suite1, suite2))
# unittest.TextTestRunner(verbosity=2).run(alltests)

# COMMAND ----------

if __name__ == '__main__':
   log_file = 'log_file.txt'
   with open(log_file, "w") as f:
       runner = unittest.TextTestRunner(f)
       unittest.main(testRunner=runner)

# COMMAND ----------

import unittest, sys

class TestOne(unittest.TestCase):

    def setUp(self):
        self.var = 'Tuesday'
    def tearDown(self):
        self.var = None 



class BasicTestOne(TestOne):

    def runTest(self):

        TestOne.setUp(self)
        self.assertEqual(self.var, 'Tuesday')



class AbsoluteMoveTestSuite(unittest.TestSuite):

    # Tests to be tested by test suite
    def makeAbsoluteMoveTestSuite():
        suite = unittest.TestSuite()
        suite.addTest(TestOne("BasicTestOne"))

        return suite 

    def suite():
        return unittest.makeSuite(TestOne)


if __name__ == '__main__':
    unittest.main()

# COMMAND ----------

cov = coverage.Coverage()
cov.start()

# suite =  unittest.TestLoader(verbosity=2).loadTestsFromTestCase(Testmodule1)      
suite =  unittest.TestLoader().loadTestsFromTestCase(Testmodule1)
#runner = xmlrunner.XMLTestRunner(output='/dbfs/tests')
#runner.TextTestRunner(verbosity=2).run(suite)
alltests = unittest.TestSuite((suite))
print(alltests)
varout= unittest.TextTestRunner(verbosity = verbosity).run(alltests)
#print(varout)
print(cov)
cov.stop()
cov.save()
cov.html_report(directory='/dbfs/tests/covhtml')
print(cov)

# COMMAND ----------

cov = coverage.Coverage()
cov.start()
# suite =  unittest.TestLoader(verbosity=2).loadTestsFromTestCase(Testmodule1)      
suite =  unittest.TestLoader().loadTestsFromTestCase(Testmodule1)
#runner = xmlrunner.XMLTestRunner(output='/dbfs/tests')
#runner.TextTestRunner(verbosity=2).run(suite)
alltests = unittest.TestSuite((suite))
unittest.TextTestRunner(verbosity=2).run(alltests)

cov.stop()
cov.save()
cov.html_report(directory='/dbfs/tests/covhtml')

# COMMAND ----------

import unittest
import xmlrunner
import coverage

def run_test_all():
    """
    Runs all the tests
    """
    test_classes_to_run = [MainUnitTests]
    loader = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    all_suite = unittest.TestSuite(suites_list)

    runner = xmlrunner.XMLTestRunner (
        output="/dbfs/tests/testreport.xml"
    )
    runner.run(all_suite)


# COMMAND ----------

run_test_all()