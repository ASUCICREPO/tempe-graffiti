import os
import shutil
import pika
import boto3
import datetime
import time
import logging
import json
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
bucket = "report-graffiti"
datetoday = datetime.date.today()
obj_path = datetoday.strftime('%Y/%m/%d/')
graffiti_dir = os.expanduser("~/graffiti") # 'C://cic//tempe-graffiti//sagemaker-graffiti-images//testinference' 

# RabbitMQ Host
credentials = pika.PlainCredentials('admin', '05rX20@qmR!',erase_on_connect=True)
parameters = pika.ConnectionParameters( host='52.3.176.47', # elastic ip
                                       port=5672,
                                       virtual_host='/host1',
                                       socket_timeout=2,
                                       credentials=credentials,
                                       heartbeat=600,
                                       blocked_connection_timeout=300)

def upload_graffiti(filename, key):
    try:
        response = s3_client.upload_file(filename, bucket, key)
    except ClientError as e:
        logging.error(e)
        return False
    return True
def make_connection():
    connection = pika.BlockingConnection(parameters)
    #Create a new channel with the next available channel number or pass in a channel number to use
    ch = connection.channel()
    #Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
    ch.queue_declare(queue='graffiti-queue',durable=True)
    return ch

connected = False
while True:
    if not connected:
        channel = make_connection()
        connected = True
    try:
        images = os.listdir(graffiti_dir)
        if images:
            for image in images:
                key = obj_path+image
                filename = os.path.join(graffiti_dir, image)
                resp = upload_graffiti(filename, key)
                if resp:
                    image_s3_url = "https://{0}.s3.amazonaws.com/{1}".format(bucket,key)
                    payload = { "image": image_s3_url,
                                "geolocation": "33.4255104, -111.9400054" #sample
                                }
                    try:
                        channel.basic_publish (exchange='graffiti-exc', routing_key='graffiti', body=json.dumps(payload),
                                            properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2))
                        try:
                            os.remove(filename)
                        except Exception as err:
                            print(err,"\ncould not remove image from captured dir",image)
                    # Recover on all connection errors
                    except:
                        connected = False
                        continue
                    
        else:
            time.sleep(10)
            try:
                print("Message Count",channel.queue_declare(queue="graffiti-queue", durable=True).method.message_count)
            except pika.exceptions.UnroutableError as e:
                connected = False
                continue
    except Exception as e:
        logging.error(e)