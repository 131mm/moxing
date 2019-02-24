import asyncio
from redis import Redis

rds = Redis(host='localhost',port=6379,db=0)

class Producer():
	def produce(self,fid,page):
		msg = '{}_{}'.format(fid,str(page))
		key = 'moxing_msg'
		rds.lpush(key,msg.encode('utf-8'))
		
def main(argv):
	import getopt
	fid = '41'
	begin = 2
	jump = 3
	number = 10
	try:
		opts, args = getopt.getopt(argv, "f:b:j:n:",["fid=", "begin=", "jump=" ,"number="])
	except getopt.GetoptError:
		print('Error')
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-f", "--fid"):
			fid = arg
		elif opt in ("-b", "--begin"):
			begin = int(arg)
		elif opt in ("-j", "--jump"):
			jump = int(arg)
		elif opt in ("-n", "--number"):
			number = int(arg)
	pro = Producer()
	for i in range(begin,number,jump):
		print(i)
		pro.produce(fid,i)
		print('done',i)

if __name__ == '__main__':
	import sys
	main(sys.argv[1:])