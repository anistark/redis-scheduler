print(' -- Test Started -- ')

from RedisScheduler import RedisScheduler

from time import time, sleep
import json

listener = RedisScheduler()
listener.start_listening(subscribe_channel='__keyevent@0__:expired')

setter = RedisScheduler()

key = str(int(time()))
value = json.dumps({'email_to': 'anirudha@venturesity.com'})
scheduled_time = '2017-02-25T12:30:00+05:30'
setter.register_event(key, value, scheduled_time)

print(' -- Test Ended -- ')
