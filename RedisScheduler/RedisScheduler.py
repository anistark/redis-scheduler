import redis, json, multiprocessing, pytz, uuid, boto3, botocore
from datetime import datetime, timezone
import dateutil.parser
from dateutil.tz import *


class RedisScheduler:

    def __init__(self, host='localhost', port=6379, path=None, db=0, password=None):
        try:
            if path:
                self.redis_client = redis.StrictRedis(path)
            else:
                self.redis_client = redis.StrictRedis(host=host, port=port)
            if password:
                self.redis_client.auth(password)
            if db:
                self.redis_client.select(db)
            print(' -- Redis Connection Success -- ')
        except Exception as e:
            print(' -- Redis Connection Failed -- ')
            print(e)


    def add_key(self, key, value, ttl=604800):
        try:
            print(' -- Adding Key -- ')
            key_added = self.redis_client.set(key, '', ex=ttl)
            shadow_key_added = self.redis_client.set('_' + key, value)
            print(key_added)
        except Exception as e:
            print(e)
            print(' -- Error while setting key -- ')
            key_added = False
        return key_added


    def register_event(self, value, expiry_time):
        response = False
        try:
            ttl = int(self.get_timedelta(expiry_time))
            if ttl>0:
                print(' -- Adding Key -- ')
                key = 'emails_'+str(uuid.uuid1())
                response = self.redis_client.set(key, "0", ex=ttl)
                shadow_key_added = self.redis_client.set('_' + key, value)
                print(response)
        except Exception as e:
            print(e)
            print(' -- Error while setting key -- ')
        return response


    def modify_event(self, key, value, scheduled_time):
        print('-- Modifying Event --')
        response = False
        try:
            ttl = int(self.get_timedelta(scheduled_time))
            if ttl>0:
                # Check for existing shadow key
                check_redis_key = self.redis_client.get(key)
                if check_redis_key:
                    redis_key = self.redis_client.set(key, value, scheduled_time)
                    shadow_key_added = self.redis_client.set('_' + key, value)
                else:
                    self.register_event(value, expiry_time)
        except Exception as e:
            print(e)
            print(' -- Error while setting key -- ')
        return response


    def subscribe_event(self, subscribe_channel='__keyevent@0__:expired', handler='sqs'):
        print('-- in subscribe event --')
        print(subscribe_channel, handler)
        try:
            pubsub_client = self.redis_client.pubsub()
            pubsub_client.subscribe(subscribe_channel)
            for message in pubsub_client.listen():
                expired_key = self.get_key(message['data'])
                print(' >> expired key : '+str(expired_key))
                shadow_key = '_%s' % expired_key
                try:
                    expired_key_value = self.redis_client.get(shadow_key)
                    expired_key_json = json.loads(self.get_key(expired_key_value))
                    print(' vv expired key value vv ')
                    print(expired_key_json)
                    self.send_to_sqs(expired_key_json)
                except Exception as e:
                    print(e)
                self.redis_client.delete(shadow_key)
        except Exception as e:
            print(e)


    def get_key(self, s):
        string = s
        if isinstance(s, bytes):
            string = s.decode('utf-8')
        return string


    def start_listening(self, subscribe_channel='__keyevent@0__:expired', handler='sqs'):
        print(' -- listener initiating -- ')
        print(subscribe_channel, handler)
        try:
            listener_service = multiprocessing.Process(target=self.subscribe_event, args=(subscribe_channel, handler,))
            listener_service.start()
        except Exception as e:
            print(e)
        print(' -- listener initiated -- ')


    def get_timedelta(self, timestamp):
        # current_time = datetime.now(pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S%z')
        current_time = datetime.now(tzutc())
        # parsed_timestamp = datetime.strptime(''.join(timestamp.rsplit(':', 1)), '%Y-%m-%dT%H:%M:%S%z')
        parsed_timestamp = dateutil.parser.parse(timestamp)
        # parsed_timestamp_in_utc = datetime_obj.astimezone(tz=timezone.utc)
        parsed_timestamp_in_utc = parsed_timestamp.astimezone(tzutc())
        return (parsed_timestamp_in_utc-current_time).total_seconds()


    def set_sqs_keys(self, access_key, secret_key, queue_name, region='ap-south-1'):
        try:
            self.boto3_client = boto3.client(
                    'sqs',
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key,
                    region_name=region
            )
            self.queue_url = self.boto3_client.get_queue_url(QueueName=queue_name)['QueueUrl']
        except Exception as e:
            print(e)
            print('^^ Some Error in connection to aws sqs ^^')


    def send_to_sqs(self, msg):
        print('-- Sending to SQS --')
        try:
            response = self.boto3_client.send_message(
                    QueueUrl=self.queue_url,
                    MessageBody=json.dumps(msg)
            )
            print('-- Sent to SQS --')
        except Exception as e:
            print(e)
            print('^^ Some Error in sending to sqs ^^')
