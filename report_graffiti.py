import os
import pika
import boto3
import datetime
import time
import logging
import json
import base64

from botocore.exceptions import ClientError

s3_client = boto3.client('s3')
# s3_resource = boto3.resource('s3')
bucket = "report-graffiti"

datetoday = datetime.date.today()
fmt_date = datetoday.strftime('%Y/%m/%d')
graffiti_dir = os.path.expanduser("~/graffiti") # 'C://cic//tempe-graffiti//sagemaker-graffiti-images//testinference' # 

logfile = 'logs/rabbit-{}.log'.format(fmt_date.replace('/','-'))
logging.basicConfig(filename=logfile,level=logging.INFO)



def get_rabbitmq_creds():

    secret_name = "rabbitmq_credentials"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return secret
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret

def upload_graffiti(filename, key):
    try:

        # object_acl = s3_resource.ObjectAcl(bucket,key)
        # response = object_acl.put(ACL='public-read')
        response = s3_client.upload_file(filename, bucket, key, ExtraArgs={'ACL':'public-read', 'ContentType':'image/jpeg'})
        # bucket.upload_file(filename, key, ExtraArgs={'ACL':'public-read'})
    except ClientError as e:
        logging.error("Upload object error"+str(e))
        return False
    return True
def make_connection():
# RabbitMQ Host
    credentials = json.loads(get_rabbitmq_creds())
    (user,pswd), = credentials.items()
    credentials = pika.PlainCredentials(user, pswd, erase_on_connect=True)
    parameters = pika.ConnectionParameters( host='52.3.176.47', # aws elastic ip for ec2 instance hosting rabbitmq
                                       port=5672,
                                       virtual_host='/host1',
                                       socket_timeout=2,
                                       credentials=credentials,
                                       heartbeat=600,
                                       blocked_connection_timeout=300)


    connection = pika.BlockingConnection(parameters)
    # Create a new channel with the next available channel number or pass in a channel number to use
    ch = connection.channel()
    # Declare queue, create if needed. This method creates or checks a queue. 
    # When creating a new queue the client can specify various properties that control the durability of the queue and its contents,
    # and the level of sharing for the queue.
    ch.queue_declare(queue='graffiti-queue',durable=True)
    return ch

connected = False

def get_geolocation():
    return "33.4255104","-111.9400054" # replace with geolocation logic

while True:
    if not connected:
        try:
            channel = make_connection()
            connected = True
        except pika.exceptions.AMQPConnectionError as connerr:
            logging.info("Cannot establish connection"+str(connerr))
    try:
        images = os.listdir(graffiti_dir)
        if images:
            for image in images:
                key = fmt_date+'/'+image
                filename = os.path.join(graffiti_dir, image)
                resp = upload_graffiti(filename, key)
                if resp:
                    image_s3_url = ("https://{0}.s3.amazonaws.com/{1}".format(bucket,key)).replace(' ','+')
                    lon,lat = get_geolocation()
                    payload = { "image": image_s3_url,
                                "geolocation": ','.join([lon,lat]) 
                                }
                    try:
                        channel.basic_publish (exchange='graffiti-exc', routing_key='graffiti', body=json.dumps(payload),
                                            properties=pika.BasicProperties(content_type='text/plain', delivery_mode=2))
                        try:
                            os.remove(filename)
                        except Exception as err:
                            logging.error(err)
                            logging.error("Could not remove image from captured dir: "+str(filename))
                    # Recover on all connection errors
                    except:
                        connected = False
                        continue
                    # print(image_s3_url)
        else:
            time.sleep(10)
            try:
                logging.info('Message Count '+str(channel.queue_declare(queue="graffiti-queue", durable=True).method.message_count))
            except Exception as e:
                connected = False
                continue
    except Exception as e:
        logging.error(e)