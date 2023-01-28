import boto3 
import json 
import logging 
from boto3.dynamodb.conditions import Key
from pyspark.sql import SparkSession
from awsglue.context import GlueContext
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)

def getSecrets(secret_name, region, secet_type='data'):
  """
  Gets database credentials from secrets manager
  """
  
  client = boto3.client("secretsmanager", region_name=region)
  
  get_secret_value_response = client.get_secret_value(
      SecretId=secret_name
  )
  
  secret = get_secret_value_response['SecretString']
  secret = json.loads(secret)
  
  secret_dict = {}
  secret_dict['engine'] = #TODO: Insert your db engine here
  secret_dict['db_user'] = secret.get("username")
  secret_dict['db_password'] = secret.get("password")
  secret_dict['db_port'] = secret.get('db_port')
  secret_dict['db_name'] = secret.get('db_name')
  secret_dict['db_host'] = secret.get('host')
  secret_dict['db_driver'] = #TODO: Insert your db driver here
  
  return secret_dict

class CustomGlueClass(object):
  
  def __init__(self, spark, GlueJobId, glueJonConfigId, glueJobTable, glueJobConfigTable, region, glueJobDetails=None):
    
    self.dynamodb = boto3.resource.('dynamodb', region_name=region)
    self.spark = spark
    self.glueJobId = GlueJobId
    self.glueJobConfigId = glueJobConfigId
    self.glueJobTable = self.dynamodb.Table(glueJobTable)
    self.glueJobConfigTable = self.dynamodb.Table(glueJobConfigTable)
    self.region = region
    self.glueJobDetails = glueJobDetails
    
   
class SparkSession(object):
  
  def __init__(self, appName):
    self.appName = appName
    
  def getSparkSession(self):
    return SparkSession.builder.appName(self.appName).getOrCreate()
  

  
