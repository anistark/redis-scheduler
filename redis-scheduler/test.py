print(' -- Test Started -- ')

from RedisScheduler import RedisScheduler

from time import time, sleep
import json

# listener = RedisScheduler()
# handler = 'sqs'
# listener.set_sqs_keys(access_key='', secret_key='', queue_name='emails', region='ap-south-1')
# listener.start_listening(subscribe_channel='__keyevent@0__:expired', handler=handler)

setter = RedisScheduler()

value = json.dumps({"multiple":False,"emailTo":"anirudha@venturesity.com","emailSubject":"Test Subject","emailBodyText":"Test Body","emailCc":"","emailBcc":"","emailType":"general","attachments":[],"emailBody":{"body":"Hello World body!!"}})
scheduled_time = '2017-02-27T12:59:00+05:30'
setter.register_event(value, scheduled_time)

key = ''
setter.modify_event(key, value, scheduled_time)

print(' -- Test Ended -- ')
