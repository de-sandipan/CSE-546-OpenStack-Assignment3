import boto3
import requests
import time
import os

s3 = boto3.resource('s3')
client = boto3.client('s3')

# Uncomment line 10 and comment line 11 before deploying to production.
# local_folder = './RecogResults/'
local_folder = 'C:/Users/Sandy/Documents/T/CSE546/project3/RecogResults/'

#
result_bucket_name = 'cse546-grp-dynamo-project3-result-bucket' 
result_bucket = s3.Bucket(result_bucket_name)

if __name__ == "__main__":

    '''
    # Download files from S3 to local file system
    '''
    processed_list = {}

    while (True):
        for obj in result_bucket.objects.all():
            if (obj.key not in processed_list):           
                obj_path = "/" + obj.bucket_name + "/" + obj.key
                local_file_path = os.path.join(local_folder, obj.key)
                result_bucket.download_file(obj.key, local_file_path)
                print('Recognition result for ' + obj.key + ' has been downloaded')
                processed_list[obj.key] = obj.key

        print("No new recognition result file - going for a sleep")
        time.sleep(3)