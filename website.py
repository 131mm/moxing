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
		return render.home()


class Page():
    def GET(self):
    	data = web.input()
    	fid = data.get('fid','41')
    	page = data.get('page','2')
    	infos,nextpage = my_spider.get_page_list(fid=fid,page=page)
    	nextpage = '/page?fid={}&page={}'.format(fid,str(int(nextpage)+1))
    	infos={'infos':infos,'nextpage':nextpage}
    	return render.page(infos)

application=app.wsgifunc()
if __name__ == '__main__':
    app.run()
