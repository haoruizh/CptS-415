
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DoubleType, IntegerType, StructField, StructType
import os

sc = SparkContext('local', 'spark_project')
sc.setLogLevel('WARN')
spark = SparkSession.builder.getOrCreate()

def ASINtest(file,conditions,select):
    df = spark.read.format('com.databricks.spark.csv').options(header='true', inferschema='true').load(file)
    df.createOrReplaceTempView("data")
    df.filter(conditions).select(select).show()

if __name__ == "__main__":
    
    file='FINAL-ASIN-TITLE-GROUP-SALESRANK.csv'
    conditions="ASIN=0827229534"
    select="title"
    ASINtest(file,conditions,select)
