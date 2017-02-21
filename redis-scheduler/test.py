print(' -- Test Started -- ')

from RedisScheduler import RedisScheduler

from time import time, sleep
import json

listener = RedisScheduler()
listener.start_listening(subscribe_channel='__keyevent@0__:expired')

setter = RedisScheduler()

while True:
    key = str(int(time()))
    value = json.dumps({'time': time(), 'foo':{'bar': 'foo', 'baz': 3, 'bor': {'foo':'bar', 'bar': 'foo'}}})
    ttl = 2
    setter.add_key(key=key, value=value, ttl=ttl)
    sleep(3)

print(' -- Test Ended -- ')
