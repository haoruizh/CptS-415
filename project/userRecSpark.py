from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql.types import StructField,IntegerType,StringType,StructType,FloatType
from pyspark.ml.feature import StringIndexer,IndexToString
from pyspark.ml.evaluation import RegressionEvaluator


spark = SparkSession \
    .builder \
    .appName("User recommendations engine") \
    .master("local[*]") \
    .getOrCreate()

#set data type in dataframe
simpleschema = StructType([
    StructField("NUM",IntegerType(),True),
    StructField("ASIN",StringType(),True),
    StructField("customer", StringType(), True),
    StructField("ratings", IntegerType(), True),
    StructField("title", StringType(), True),
])

df = spark.read.csv("demo.csv",header=True,schema=simpleschema)
#tansform string form of title to index for titleId
stringIndexer = StringIndexer(inputCol="title", outputCol="titleId")
model = stringIndexer.fit(df)
df2 = model.transform(df)
#tansform string form of customer to index for customerId
stringIndexer2 = StringIndexer(inputCol="customer", outputCol="customerId")
model2 = stringIndexer2.fit(df2)
ratingsData = model2.transform(df2)
#sort by customerId from 0 to n,we can see a lot of same id customer
ratingsData = ratingsData.sort("customerId")
ratingsData.show()#show the final update dataframe

#start to do ALS alg to make a form of user*product
(training,test) = ratingsData.randomSplit([0.75,0.25])
als = ALS(maxIter=5, regParam=0.01, userCol="customerId", itemCol="titleId", ratingCol="ratings",
implicitPrefs=True, coldStartStrategy="drop",nonnegative=True)
model = als.fit(training)
#predictions = model.transform(test)
#predictions.show()
#evaluator = RegressionEvaluator(metricName="rmse", labelCol="ratings",predictionCol="prediction")
#rmse = evaluator.evaluate(predictions)
#print("Root-mean-square error = " + str(rmse))

#Generate top 10 item recommendations for each user
userRecommemdations = model.recommendForAllUsers(10)
#Collect the data in list
userRecommemdationsList = userRecommemdations.collect()
#Sort the list by customerId
userRecommemdationsList.sort()
#Use dic to make a customer as key, recommemd title as value

RecommemdationsDict = dict()
for key,value in userRecommemdationsList:
    RecommemdationsDict["customerID: "+str(key)] = value
#Now start to input the customer id, output will be top 10 item recommendations
customer = input('Customer id: ')
alist = RecommemdationsDict["customerID: "+customer]
print("The customer name is : ")
#show the regular customer id
ratingsData.filter("customerId=="+customer).select("customer").show(1)
print("The top ten recommendations for this user below")
#show the top 10 item recommendations
for title in alist:
    ratingsData.filter("titleId=="+str(title[0])).select("ASIN","title").show(1)

