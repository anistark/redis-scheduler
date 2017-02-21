import redis, json, multiprocessing, pytz
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


    def register_event(self, key, value, expiry_time):
        response = False
        try:
            # ttl = int(time())-int(expiry_time)
            ttl = int(self.get_timedelta(expiry_time))
            print(ttl)
            if ttl>0:
                print(' -- Adding Key -- ')
                response = self.redis_client.set(key, "0", ex=ttl)
                shadow_key_added = self.redis_client.set('_' + key, value)
                print(response)
        except Exception as e:
            print(e)
            print(' -- Error while setting key -- ')
        return response


    def subscribe_event(self, subscribe_channel='__keyevent@0__:expired'):
        try:
            pubsub_client = self.redis_client.pubsub()
            pubsub_client.subscribe(subscribe_channel)
            for message in pubsub_client.listen():
                expired_key = self.get_key(message['data'])
                print(' >> expired key : '+str(expired_key))
                shadow_key = '_%s' % expired_key
                try:
                    expired_key_value = self.redis_client.get(shadow_key)
                    print(' >> expired key value : '+ str(expired_key_value))
                    expired_key_json = json.loads(self.get_key(expired_key_value))
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


    def start_listening(self, subscribe_channel='__keyevent@0__:expired'):
        print(' -- listener initiatiating -- ')
        try:
            listener_service = multiprocessing.Process(target=self.subscribe_event, args=(subscribe_channel,))
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

