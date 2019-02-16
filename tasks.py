from celery import Celery
from redis import Redis
from spider import Spider
import json

rds = Redis(host='localhost',port=6379,db=0) 

app = Celery('tasks',broker='redis://localhost:7777/0')

spr = Spider()
@app.task
def worker(fid,page,objs):
    keys = 'moxing_'+fid+'_'+str(page)
    res = rds.get(keys)
    if not res:
        infos = spr.get_page_list_1(fid,page,objs)
        rds.set(keys,json.dumps(infos).encode('utf-8'))
    rds.expire(keys,600)

