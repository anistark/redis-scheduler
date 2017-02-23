# RedisScheduler

![license](https://img.shields.io/github/license/anistark/redis-scheduler.svg) [![pypi](https://img.shields.io/pypi/v/redis-scheduler.svg)](https://pypi.python.org/pypi/redis-scheduler)


## Install via pip

```
pip install redis-scheduler
```

## Usage

```
from redis-scheduler import RedisScheduler
```

### Start Listening


Initialise RedisScheduler

```
listener = RedisScheduler()
```

Set SQS keys

```
listener.set_sqs_keys(access_key='', secret_key='', queue_name='emails', region='ap-south-1')
```

Start Listening

```
listener.start_listening(handler='sqs')
```


### Registering your event

```
setter = RedisScheduler()
```

```
key = str(int(time()))
```

```
value = json.dumps({'time': time(), 'foo':{'bar': 'foo', 'baz': 3, 'bor': {'foo':'bar', 'bar': 'foo'}}})
```

#### Scheduled time for the event in iso format with timestamp

```
scheduled_time = '2017-02-25T12:30:00+05:30'
```

### Register the event to be scheduled

Register your event

```
setter.register_event(value, scheduled_time)
```

Modify your registered event

```
setter.modify_event(key, value, scheduled_time)
```


#### Contributions welcome for more handlers and enhancements. Contribution document coming soon.

