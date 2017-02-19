# Import classes from your brand new package
from RedisScheduler import RedisScheduler

# Create an object of Mammals class & call a method of it
import redis
# try:
#     r = redis.StrictRedis(host='localhost', port=6379, db=0)
#     print(' -- Redis Connection Established -- ')
#     r.set('foo', 'bar', ex=100)
#     r.get('foo')
# except Exception as e:
#     print(e)

redis_scheduler = RedisScheduler(host='localhost', port=6379)

object_added = redis_scheduler.add('food', 'Mango', 100)

# redis_scheduler.printMembers()
print(object_added)

print(' -- Test Ended -- ')
