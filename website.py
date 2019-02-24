import web
import json
import spider
from web.contrib.template import render_jinja

urls=(
    '/', 'Home',
    '/page','Page',
    '/data','Data',
)

app=web.application(urls,globals())
my_spider = spider.Spider()
render=render_jinja('templates',encoding='utf-8')

class Home():
    def GET(self):
        from producer import Producer
        pro = Producer()
        fids = ['40','41','43','44','45','46','47']
        for fid in fids:
            pro.produce(fid=fid,page=2)
        return open(r'templates/home.html','r').read()

class Page():
    def GET(self):
        data = web.input()
        fid = data.get('fid','41')
        return open(r'templates/page{}.html'.format(fid),'r').read()

class Data():
    def GET(self):
        data = web.input()
        fid = data.get('fid','41')
        page = int(data.get('page','2'))
        infos,nextpage = my_spider.get_page_list(fid=fid,page=page,objs=[])
        this_url = '/data?fid={}&page={}'.format(fid,str(page))
        next_url = '/data?fid={}&page={}'.format(fid,str(nextpage+1))
        infos={'infos':infos,'nextpage':next_url,'thispage':this_url}
        return json.dumps(infos)



application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
