import os.path
import json
import boto3
from botocore.vendored import requests
import pandas as pd




def download_file_to_local(url):
    # URL which needs to be download
    url = "https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls"
    r = requests.get(url) # create HTTP response object
    print("Request received")
    os.chdir('/tmp/')
    with open("ISO_file.xlsx",'wb') as f:
         #saving content in file(binary format)
        f.write(r.content)
    
    
def write_file_to_s3(file_obj, bucket_name, s3_key):
    s3 = boto3.client('s3')
    s3.put_object(
        Body=file_obj,
        Bucket=bucket_name,
        Key=s3_key)
    return



def lambda_handler(event, context):
    # TODO implement
    #DOWNLOAD FILE
    
    context = "https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.xls"
    #call download function
    download_file_to_local(context)
    print("File Downloaded")
    
    #PROCESS FILE
    file = 'ISO_file.xlsx'
    # Loading spreadsheet
    xl = pd.ExcelFile(file)
    
    # Print the sheet names
    print(xl.sheet_names)
    
    # Load required sheet into a DataFrame by name
    df = xl.parse('MICs List by CC')
    
    # Converting each row of DF into dict with key as col name
    my_dict = df.to_dict('record')
    
    #Converting list of dict into json obj
    json_obj = json.dumps(my_dict)
    
    #WRITE FILE TO S3
    #call write file to s3 function
    write_file_to_s3(json_obj,'astro-datalake-nprod-common','test/mytest.json')
    return 'Hello from Lambda'


