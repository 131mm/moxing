import web
import spider
import json
from redis import Redis
from producer import Producer

urls=(
    '/', 'Home',
    '/data', 'Data',
)

app=web.application(urls,globals())
my_spider = spider.Spider()
pro = Producer()
rds = Redis(host='localhost',port=6379) 

class Home():
    def GET(self):
        fids = ['40','41','43','44','45','47']
        for fid in fids:
            pro.produce(fid=fid,page=2)
        return open(r'./home.html', 'r').read()


class Data():
    def GET(self):
        data = web.input()
        fid = data.get('fid','41')
        page = int(data.get('page','2'))
        keys = 'moxing_'+fid+'_'+str(page)
        res = rds.get(keys)
        if res:
            infos,nextpage = json.loads(res.decode('utf-8'))
        else:
            infos,nextpage = my_spider.get_page_list(fid=fid,page=page,objs=[])
        pro.produce(fid=fid,page=nextpage+1)
        next_url = '/data?fid={}&page={}'.format(fid,str(nextpage+1))
        infos={'infos':infos,'nextpage':nextpage,'next_url':next_url}
        return json.dumps(infos)

application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
