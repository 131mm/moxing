from redis import Redis

rds = Redis(host='localhost',port=6379,db=0)

class Producer():
	def produce(self,fid,page):
		msg = '{}_{}'.format(fid,str(page))
		key = 'moxing_msg'
		rds.lpush(key,msg.encode('utf-8'))