import redis
from time import time, sleep
import multiprocessing
from random import choice
import json
import codecs
reader = codecs.getreader("utf-8")

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
    # Default ttl is 1 week (604800 sec)

    def add_key(self, key, value, ttl=604800):
        print(' -- Adding RS key -- ')
        print(key, value, ttl)
        try:
            key_added = self.redis_client.set(key, value, ex=ttl)
            shadow_key_added = self.redis_client.set('_' + key, value)
        except Exception as e:
            print(e)
            print(' -- Error while setting key -- ')
            key_added = False
        return key_added

    def subscribe_event(self, subscribe_channel='__key@0__:expired'):
        try:
            pubsub_client = self.redis_client.pubsub()
            pubsub_client.subscribe(subscribe_channel)
            message = pubsub_client.get_message()
            print(message)
            print(' +++++++ ')
            for message in pubsub_client.listen():
                expired_key = self.get_key(message['data'])
                shadow_key = '_%s' % expired_key
                expired_key_value = self.redis_client.get(shadow_key)
                try:
                    expired_key_json = json.loads(expired_key_value.decode('utf-8'))
                    print (expired_key_json)
                    print (json.dumps(expired_key_json, indent=4))
                except Exception as e:
                    print(e)
                print('key expired', expired_key, expired_key_value)
                self.redis_client.delete(shadow_key)
                print(' __ ')
        except Exception as e:
            print(e)

    def get_key(self, s):
        if isinstance(s, str):
            string = s
        elif isinstance(s, bytes):
            string = s.decode('utf-8')
        else:
            string = s
        return string

if __name__ == '__main__':
    listener = RedisScheduler()
    listener_service = multiprocessing.Process(name='my_service', target=listener.subscribe_event, args=('__keyevent@0__:expired',))
    setter = RedisScheduler()
    listener_service.start()
    while True:
        setter.add_key(str(int(time())), json.dumps({'time': time(), 'foo':{'bar': 'foo', 'baz': 3, 'bor': {'foo':'bar', 'bar': 'foo'}}}), 7)
        sleep(10)