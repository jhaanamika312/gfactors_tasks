
import pika
from pika import channel


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel= connection.channel()
channel.queue_declare(queue='hello anamika')
channel.basic_publish(exchange = '', routing_key ='hello anamika', body='Hello anamika welcome to rabbitMQ')

print("Published Message")
connection.close()

