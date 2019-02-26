from redis import Redis
from asyncspider import AsyncSpider
import json
import asyncio
from kafka import KafkaConsumer

rds = Redis(host='localhost',port=6379,db=0) 
spr = AsyncSpider()
consumer = KafkaConsumer('test',bootstrap_servers=['localhost:9092'])

async def worker(i):
	import time
	print('worker:',i)
	for msg in consumer:
		msg = msg.value.decode()
		argues = msg.split('_')
		fid, page= argues[0],int(argues[1])
		keys = 'moxing_'+fid+'_'+str(page)
		
		start = time.time()
		print('start:',fid,page)
		
		res = rds.get(keys)
		if not res:
			infos = await spr.get_page_list(fid=fid,page=page,start_page=page,objs=[])
			rds.set(keys,json.dumps(infos).encode('utf-8'))
			rds.expire(keys,600)

		end = time.time()
		print('end:  ',fid,page,end-start,'s')

if __name__ == '__main__':
	w1 = worker(1)
	w2 = worker(2)
	w3 = worker(3)
	w4 = worker(4)
	w5 = worker(5)
	workers = (w1,w2,w3,w4,w5)
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.gather(*workers))
	loop.close()
