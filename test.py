import redis
import time
import pprint

r = redis.Redis()
ts = int(time.time())
tsrange = 50000
r.delete('test')
print "from %s to %s" % (ts, ts+tsrange) 

pipe = r.pipeline(tsrange)
for i in range(tsrange):
#    p.zadd('test', ts+i, i)
    pipe.execute_command("ts.insert","test", ts+i, i)
s = time.time()
pipe.execute()
e = time.time()
insert_time = e - s

s = time.time()
for i in range(10):
    res = r.execute_command("ts.query", "test", ts, ts+tsrange)
    res_size = len(res)
    print res[0], res[-1]
    print res_size/2.0
e = time.time()
query_time = e - s

i = 0
ts_res = dict()
while res:
    ts_res[res.pop()] = res.pop()

# print pprint.pprint(ts_res)
print res_size/2.0
print "items %s:" % tsrange 
print "took %s to insert sec" % insert_time
print "took %s to query sec" % query_time
