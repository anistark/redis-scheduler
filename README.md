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

```
listener = RedisScheduler()
```

```
listener.start_listening()
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

```
setter.register_event(key, value, scheduled_time)
```

