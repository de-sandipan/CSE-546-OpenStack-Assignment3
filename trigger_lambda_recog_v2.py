import boto3
import requests
import time
import os
from multiprocessing import Pool

s3 = boto3.resource('s3')
client = boto3.client('s3')

# ingress_bucket - persistent storage of user uploaded videos

ingress_bucket_name = 'cse546-grp-dynamo-project3-ingress-bucket' 
ingress_bucket = s3.Bucket(ingress_bucket_name)

# AWS API Gateway URL
gateway_url = 'https://r9zrnq967f.execute-api.us-east-1.amazonaws.com/uploaded-video'

def trigger_api_call(file_name):
    url = gateway_url + "?bucket_name=" + ingress_bucket_name + "&file_name=" + file_name
    r = requests.post(url)
    if r.status_code != 200:
        print('sendErr: '+r.url)
    else:
        print(file_name + " sent to face recognition module; process id: " + str(os.getpid()))

if __name__ == '__main__':
    processed_list = {}
    p = Pool(10)
    while(True):
        obj_list = ingress_bucket.objects.all()
        new_object_list = []
        for obj in obj_list:
            if (obj.key not in processed_list):
                processed_list[obj.key] = obj.key
                new_object_list.append(obj.key)
        p.map(trigger_api_call, new_object_list)
        print("No new file - going for a sleep")
        time.sleep(3)