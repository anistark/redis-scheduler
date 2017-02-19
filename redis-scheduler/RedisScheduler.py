import redis


class RedisScheduler:
    def __init__(self, host='localhost', port=6379, path=None, db=0, password=None, options=None):
        ''' Constructor for this class. '''
        # Create some member animals
        self.members = ['Tiger', 'Elephant', 'Wild Cat']
        try:
            if path:
                redis_client = redis.StrictRedis(path, options)
            else:
                redis_client = redis.StrictRedis(port, host, options);

            if password:
                redis_client.auth(password)

            if db:
                redis_client.select(db)
            self.redis_client = redis_client
            print(' -- Redis Connection Success -- ')
        except Exception as e:
            print(' -- Redis Connection Failed -- ')
            print(e)
        print(' == out == ')


    # def printMembers(self):
    #     print('Printing members of the Mammals class')
    #     for member in self.members:
    #         print('\t%s ' % member)


    def add(self, key, value, ttl=604800):
        # Default ttl is 1 week
        print(' -- Adding RS event -- ')
        object_added = self.redis_client.set(key, value, ex=ttl)
        return object_added

