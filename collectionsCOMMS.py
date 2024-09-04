import boto3
import pandas as pd
from datetime import datetime
from time import gmtime, strftime
from awsglue.utils import getResolvedOptions
import sys
import requests
import json
 
url = "https://dev-gw.integration.api.wfscloud.co.za/comms/freetext/email"



args = sys.argv
params = getResolvedOptions(sys.argv, ['file_key'])

file_key = params['file_key']
file_key = str(file_key).replace("+"," ")

if file_key.endswith(" 00.csv") or file_key.endswith(" 04.csv") or file_key.endswith(" 08.csv") or file_key.endswith(" 12.csv") or file_key.endswith(" 16.csv") or file_key.endswith(" 20.csv"):
    
    bucket="s3://euw1-prd-data-lake-acceltr01-clickatell-whatsapp-bucket/"
    bucket_prod="s3://wfs-production/chatflow/"
    bucket_prod_chatdesk="s3://wfs-production/chatdesk/"
    key_output="wfs/exl/collections/"
    
    if file_key.startswith("wfs/chatdesk_detail/"):
        print("No need!!!")
        subject = "Collection Chatflow status"
        content = "Dear Team,\n\nThere was no need to record the data, as it pertains to chatdesk rather than chatflow. \n\nBest regards,\n"
        pass
        # df=pd.read_csv(bucket+file_key,header=0,encoding='utf-8',escapechar='\\')
        # if df.empty:
        #     print('DataFrame is empty!')
        # else:
        #     df.to_csv(bucket_prod_chatdesk+str(file_key).split("/")[2],index=False)
        #     print("Data written to final s3 bucket for Chatdesk")
    elif file_key.startswith("wfs/chatflow_detail/"):
        df=pd.read_csv(bucket+file_key,header=0,encoding='utf-8',escapechar='\\')
        df_filtered=df[(df["flow_name"]=="Collections") | (df["flow_name"]=="AgentDesk2")]
        print(df_filtered)
        if df_filtered.empty:
            print('DataFrame is empty!')
            #Comms for chatflow s3 bucket when it is empty
            subject = "Collection Chatflow Status"
            content = "Dear Team,\n\nDataFrame is empty! \n\nBest regards,\n"
        else:
            df_filtered.to_csv(bucket+key_output+str(file_key).split("/")[2],index=False)
            df_filtered.to_csv(bucket_prod+str(file_key).split("/")[2],index=False)
            print("Data written to final s3 bucket for Chatflow")
#Comms for chatflow s3 bucket when the data is written
            subject = "Collection Chatflow Success"
            content = "Dear Team,\n\nData written to final s3 bucket for Chatflow \n\nBest regards,\n"
    else:
        print("File type not defined")
        subject = "Collection Chatflow Failed"
        content = "Dear Team,\n\nFile type not defined \n\nBest regards,\n"

else:
    print("No need to push")
#Comms for when there was no need to push any data
    subject = "Collection Chatflow status"
    content ="Dear Team,\n\nNo need to push the data \n\nBest regards,\n"


#COMMS
headers = {
  'x-api-key': 'xxxxx', 
  'Content-Type': 'application/json',
  'Authorization': 'Bearer xxxxx'
} 

#Email Template
payload = payload = json.dumps({
    "client": "Collections",
    "emailAddress": "mpumelelongozo@wfs.co.za",
    "subject": subject,
    "content": content
    })
response = requests.request("POST", url, headers=headers, data=payload)
 
print(response.text)