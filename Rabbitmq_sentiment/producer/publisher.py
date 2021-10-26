try:
    import pika

except Exception as e:
    print("Sone Modules are missings {}".format_map(e))



class RabbitMq(object):

    def __init__(self, queue='hello'):

    

        self._connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self._channel = self._connection.channel()
        self.queue= queue
        self._channel.queue_declare(queue=self.queue)

    def publish(self, payload ={}):

        """
        :param payload: JSON payload
        :return: None
        """

        self._channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=str(payload))

        print("Published Message")
        self._connection.close()


if __name__ == "__main__":
    server = RabbitMq(queue='hello')
    server.publish(payload={"Data":"Hello"})