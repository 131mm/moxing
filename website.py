from sanic import Sanic
from sanic.response import json,html,file
import asyncspider

app = Sanic()

my_spider = asyncspider.AsyncSpider()

@app.route('/')
async def home(request):
    from producer import Producer
    pro = Producer()
    fids = ['40','41','43','44','45','46','47']
    for fid in fids:
        pro.produce(fid=fid,page=2)
    return await file('home.html')

@app.route('/data')
async def data(request):
        data = request.args
        fid = data.get('fid','41')
        page = int(data.get('page','2'))
        infos,nextpage = await my_spider.get_page(fid=fid,page=page,objs=[])
        this_url = '/data?fid={}&page={}'.format(fid,str(page))
        next_url = '/data?fid={}&page={}'.format(fid,str(nextpage+1))
        infos={'infos':infos,'nextpage':next_url,'thispage':this_url}
        return json(infos)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8800)
