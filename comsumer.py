from redis import Redis
from asyncspider import AsyncSpider
import json
import asyncio
from kafka import KafkaConsumer

rds = Redis(host='localhost',port=6379,db=0) 
spr = AsyncSpider()
consumer = KafkaConsumer('test',bootstrap_servers=['localhost:9092'])

async def main(i):
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
			await spr.get_page_list(fid=fid,page=page,start_page=page,objs=[])

		end = time.time()
		print('end:  ',fid,page,end-start,'s')

if __name__ == '__main__':
	w1 = main(1)
	w2 = main(2)
	w3 = main(3)
	w4 = main(4)
	w5 = main(5)
	workers = (w1,w2,w3,w4,w5)
	loop = asyncio.get_event_loop()
	# loop.run_until_complete(w1)
	loop.run_until_complete(asyncio.gather(*workers))
	loop.close()
