from redis import Redis
from spider import Spider
import json
import time
import threading
import gc
import logging

logging.basicConfig(filename='work.log',format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)
rds = Redis(host='localhost',port=6379) 
spr = Spider()
def worker():
	while True:
		msg = rds.brpop('moxing_msg')
		msg = msg[1].decode('utf-8')
		argues = msg.split('_')
		fid, page= argues[0],int(argues[1])
		keys = 'moxing_'+fid+'_'+str(page)
		start = time.time()
		res = rds.get(keys)
		if not res:
			logging.info('getting '+fid+'-'+str(page))
			infos = spr.get_page_list(fid=fid,page=page,objs=[])
			rds.set(keys,json.dumps(infos).encode('utf-8'))
			rds.expire(keys,600)
			del infos
		del res
		gc.collect()

		end = time.time()
		logging.info('end '+fid+'-'+str(page)+' '+str(end-start)+'s')

def main():
	loop = []
	for i in range(5):
		t = threading.Thread(target=worker)
		loop.append(t)
	for i in loop:
		i.start()
	for i in loop:
		i.join()

if __name__ == '__main__':
	main()
