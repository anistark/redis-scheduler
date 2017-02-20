print(' -- Test Started -- ')

from RedisScheduler import RedisScheduler

from time import time, sleep
import multiprocessing, json

listener = RedisScheduler()
listener_service = multiprocessing.Process(target=listener.subscribe_event, args=('__keyevent@0__:expired',))
setter = RedisScheduler()
listener_service.start()

while True:
    key = str(int(time()))
    value = json.dumps({'time': time(), 'foo':{'bar': 'foo', 'baz': 3, 'bor': {'foo':'bar', 'bar': 'foo'}}})
    ttl = 7
    setter.add_key(key, value, ttl)
    sleep(10)

print(' -- Test Ended -- ')
