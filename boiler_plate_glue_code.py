import sys
import boto3
import json
import os
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext 
from awsglue.context import GlueContext
from awsglue.job import Job

from utilities import *
import logging


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)


def getGlueParameters():
  glueParameters = getResolvedOptions(
    sys.argv,
    [
        'glue-job-name',
        'glue-job-id,
        'glue-job-configuration-id',
        'glue-job-table',
        'glue-job-config-table',
        'glue-job-configuration-name',
        'region'
    ]
  )
  
  return glueParameters

def getGlueConfigDetails(spark, glueParameters):
  myCustomGlue = CustomGlue(
      spark,
      glueParameters['glue-job-id'],
      glueParameters['glue-job-configuration-id'],
      glueParameters['glue-job-table'],
      glueParameters['glue-job-config-table'],
      glueParameters['region']
  )
  
  myCustomGlue.getglueJobConfigurationDetails()
  glueConfiguration = myCustomGlue.glueJobDetails[0]
  
  return glueConfiguration

def process_data(**kwargs):
  #TODO: Insert your business logic here
  pass

def update_last_exract_date_time(extract_date_time, **kwargs):
  GlueJobConfigurationTable = kwargs['glue_job_config_table']
  GlueJobConfigurationId = kwargs['glue_job_configuration_id']
  GlueJobConfigurationName = kwargs['glue_job_configuration_name']
  
  dynamodb = boto3.resource('dynamodb')
  dynamodb_table = dynamodb.Table(GlueJobConfigurationTable)
  
  response = dynamodb_table.update_item(
    Key={
        'GlueJobConfigurationId': GlueJobConfigurationId,
        'GlueJobConfigurationName': GlueJobConfigurationName
    },
    UpdateExpression = 'set LastExtractiontimestamp=:ledt',
    ExpressionAttributeValues={
        ':ledt': extract_date_time
    },
    ReturnValues = 'UPDATED_NEW'
  )
  
  logging.info(response)

def main():
  glueParameters = getGlueParameters()
  glueConfiguration = getGlueConfigDetails(spark, glueParameters)
  
  glue_config = glueConfiguration['GlueCustom']
  glue_config['LastExtractDateTime'] = glueConfiguration['LastExtractDateTime']
  last_extract_ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
  
  process_data(**glue_config)
  
  update_last_extract_date_time(last_extract_ts, **glueParameters)
  
  
if __name__ == "__main__":
  main()
  job.commit()
      
