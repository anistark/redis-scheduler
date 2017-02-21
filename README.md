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

### Adding event key

```
setter = RedisScheduler()
```

```
key = str(int(time()))
```

```
value = json.dumps({'time': time(), 'foo':{'bar': 'foo', 'baz': 3, 'bor': {'foo':'bar', 'bar': 'foo'}}})
```

```
ttl = 200  # 200sec
```

```
setter.add_key(key=key, value=value, ttl=ttl)
```

