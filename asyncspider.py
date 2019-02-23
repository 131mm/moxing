import requests
from bs4 import BeautifulSoup as bs
from redis import Redis
import json
import aiohttp
import asyncio

rds = Redis(host='127.0.0.1',port=6379,db=0)

class AsyncSpider():
	def __init__(self):
		suf = rds.get('moxing_suf')
		self.suffix = suf.decode() if suf else 'zone'
		self.prefix = '''https://www.moxing.{}/'''.format(self.suffix)
		self.UA = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'''
		self.headers = {'user-agent':self.UA}

	async def get_page_list(self,fid,page=2,start_page=2,objs=[]):
		limit = self.get_limit(fid=fid)
		url = '''{}forum.php?mod=forumdisplay&fid={}&page={}'''.format(self.prefix,fid,str(page))
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as web:
				text = await web.text()
		soup = bs(text,'lxml')
		items = soup.select('#waterfall > li')
		for item in items:
			try:
				if not item:
					continue
				comments = '0'
				comments = item.cite.a.contents[0]
				if int(comments)<limit:
					continue
				a = item.a
				href = a['href']
				href = self.prefix + href
				title = a['title']
				img = item.img['src']
				obj={'comments':comments, 'href':href, 'title':title, 'img':img}
				objs.append(obj)
			except: pass
		if len(objs)>=10:
			infos = (objs,page)
			keys = 'moxing_'+fid+'_'+str(start_page)
			rds.set(keys,json.dumps(infos).encode('utf-8'))
			rds.expire(keys,600)
			print('gotall',fid,start_page,len(objs),'page_now:',page)
		else:
			page +=1
			await self.get_page_list(fid=fid,page=page,start_page=start_page,objs=objs)
	def get_limit(self,fid):
		limits = {
		'40':50,
		'41':30,
		'43':30,
		'44':30,
		'45':30,
		'46':30,
		'47':80,
		}
		return limits.get(fid)



if __name__ == '__main__':
	spr = AsyncSpider()
	async def run():
		infos = await spr.get_page_list(fid='41',page=2,objs=[])
		return infos

	co = run()
	tasks = [asyncio.ensure_future(co)]
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))
	for task in tasks:
		print('Task ret: ', task.result())
	#fun_list = (spr.get_page_list_2(fid='41',page=i,objs=[]) for i in range(4,10))
	#loop.run_until_complete(asyncio.gather(*fun_list))