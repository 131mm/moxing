from redis import Redis
from spider import Spider
import json
import time
import threading

rds = Redis(host='localhost',port=6379) 
spr = Spider()
def worker():
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
			infos = spr.get_page_list(fid=fid,page=page,objs=[])
			rds.set(keys,json.dumps(infos).encode('utf-8'))
			rds.expire(keys,600)
			print('job done',msg,len(infos[0]))

		end = time.time()
		print('end:  ',fid,page,end-start,'s')

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
