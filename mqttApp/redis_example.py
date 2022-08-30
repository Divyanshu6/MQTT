import redis
from datetime import datetime

r = redis.Redis()

keys=set()
for key in r.scan_iter("GPM*"):
    # delete the key
    keys.add(key)

print(len(keys))
# for i in keys:
#     print(r.get(i))