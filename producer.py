from kafka import KafkaProducer
from kafka.errors import KafkaError
import asyncio

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

class Producer():
	def produce(self,fid,page):
		msg = '{}_{}'.format(fid,str(page))
		future = producer.send('test',msg.encode())
		try:
			record = future.get(timeout=10)
		except kafkaError:
			return 1
if __name__ == '__main__':
	pro = Producer()
	for i in range(2,3):
		print(i)
		pro.produce('41',i)
		print('done',i)