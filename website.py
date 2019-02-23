import web
import spider
from web.contrib.template import render_jinja

urls=(
    '/', 'Home',
    '/page', 'Page',
)

app=web.application(urls,globals())

render=render_jinja('templates',encoding='utf-8')

my_spider = spider.Spider()

class Home():
    def GET(self):
        from producer import Producer
        pro = Producer()
        fids = ['40','41','43','44','45','46','47']
        for fid in fids:
            pro.produce(fid=fid,page=2)
        return render.home()


class Page():
    def GET(self):
        data = web.input()
        fid = data.get('fid','41')
        page = int(data.get('page','2'))
        infos,nextpage = my_spider.get_page_list(fid=fid,page=page,objs=[])
        next_url = '/page?fid={}&page={}'.format(fid,str(nextpage+1))
        infos={'infos':infos,'nextpage':next_url}
        return render.page(infos)

application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
