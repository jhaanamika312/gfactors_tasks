import pika
    
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel= connection.channel()
channel.queue_declare(queue='hello anamika')

def callback(ch, method, properties, body):
    print(" [x] Recieved %r" %body)

channel.basic_consume(queue='hello anamika',on_message_callback= callback, auto_ack=True)

print(' [*] waiting for messages. To exit press CTRL+C')
channel.start_consuming()