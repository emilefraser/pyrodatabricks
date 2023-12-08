# Databricks notebook source

#pyspark imports
import pyspark.sql.functions as F
from pyspark.sql.window import Window


# COMMAND ----------

#module
class calculator:

	def __init__(self, x = 10, y = 8, dbutils = None, spark = None):
		self.x = x
		self.y = y
		self.dbutils = dbutils
		self.spark = spark
			
	def add(self, x = None, y = None):
		"""add function"""
		if x == None:
			x = self.x
		if y == None:
			y = self.y			
		return x+y

	def subtract(self, x = None, y = None):
		"""subtract function"""
		if x == None:
			x = self.x
		if y == None:
			y = self.y	
		return x-y

	def multiply(self, x = None, y = None):
		"""multiply function"""
		if x == None:
			x = self.x
		if y == None:
			y = self.y			
		return x*y

	def devide(self, x = None, y = None):
		"""devide function"""
		if x == None:
			x = self.x
		if y == None:
			y = self.y			
		if y == 0:
			raise ValueError('cannot devide by zero')
		else:
			return x/y