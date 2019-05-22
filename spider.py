import requests
from bs4 import BeautifulSoup as bs
from redis import Redis
import json


rds = Redis(host='127.0.0.1',port=6379,db=0)

class Spider():

	def __init__(self):
		suf = rds.get('moxing_suf')
		self.suffix = suf.decode() if suf else 'fyi'
		self.prefix = '''https://www.moxing.{}/'''.format(self.suffix)
		self.UA = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'''
		self.headers = {'user-agent':self.UA}

	def get_page_list(self,fid,page=2,objs=[]):
		limit = self.get_limit(fid=fid)
		url = '''{}forum.php?mod=forumdisplay&fid={}&page={}'''.format(self.prefix,fid,str(page))
		web = requests.get(url,headers=self.headers)
		soup = bs(web.text,'lxml')
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
			return objs,page
		else:
			return self.get_page_list(fid=fid,page=page+1,objs=objs)

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
	import pdb
	pdb.set_trace()
	app = Spider()
	print(app.get_page_list('40'))
