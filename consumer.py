from redis import Redis
from asyncspider import AsyncSpider
import json
import asyncio

rds = Redis(host='localhost',port=6379,db=0) 
spr = AsyncSpider()

async def worker(i):
	import time
	print('worker:',i)
	while True:
		msg = rds.rpop('moxing_msg')
		if not msg:
			time.sleep(1)
			continue
		msg = msg.decode('utf-8')
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
			print('job done',msg,len(infos[0]))

		end = time.time()
		print('end:  ',fid,page,end-start,'s')

if __name__ == '__main__':
	import time
	for i in range(10):
		asyncio.ensure_future(worker(i))
	loop = asyncio.get_event_loop()
	try:
		loop.run_forever()
	except KeyboardInterrupt as e:
		print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
		loop.stop()
		loop.run_forever()
	finally:
		loop.close()