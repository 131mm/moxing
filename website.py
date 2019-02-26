from sanic import Sanic
from sanic.response import json,html,file
from sanic_jinja2 import SanicJinja2
import asyncspider

app = Sanic()
jinja = SanicJinja2(app)

my_spider = asyncspider.AsyncSpider()

@app.route('/content.html')
async def content(request):
    return await file('content.html')

@app.route('/')
async def home(request):
    from producer import Producer
    pro = Producer()
    fids = ['40','41','43','44','45','46','47']
    for fid in fids:
        pro.produce(fid=fid,page=2)
    return html(open(r'home.html','r').read())

@app.route('/page')
@jinja.template('page.html')
async def page(request):
    data = request.args
    fid = data.get('fid','41')
    page = data.get('page','2')
    return {'url':'/data?fid={}&page={}'.format(fid,page)}

@app.route('/data')
async def data(request):
        data = request.args
        fid = data.get('fid','41')
        page = int(data.get('page','2'))
        infos,nextpage = await my_spider.get_page_list(fid=fid,page=page,objs=[])
        this_url = '/data?fid={}&page={}'.format(fid,str(page))
        next_url = '/data?fid={}&page={}'.format(fid,str(nextpage+1))
        infos={'infos':infos,'nextpage':next_url,'thispage':this_url}
        return json(infos)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8800)
