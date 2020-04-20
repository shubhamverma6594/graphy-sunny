import json
import pika


class Producer:
    def __init__(self, queue_config, mq_config):
        self.mq_config = mq_config
        self.config = queue_config
        self.connection = self._create_connection()
        self.channel = self.connection.channel()

    def publish(self, message):
        body=json.dumps(message)

        if (not self.connection) or (not self.connection.is_open):
            self.connection = self._create_connection()
            self.channel = self.connection.channel()
 
        self.channel.exchange_declare(exchange=self.config['exchangeName'],
                                     passive=True)
        self.channel.basic_publish(exchange=self.config['exchangeName'],
                                  routing_key=self.config['routingKey'],
                                  body=body)
 
        print(" [x] Sent message %r" % message)

    def _create_connection(self):
        credentials = pika.PlainCredentials(self.mq_config['userName'], self.mq_config['password'])
        parameters = pika.ConnectionParameters(self.mq_config['host'], self.mq_config['port'],
                                               self.mq_config['virtualHost'], credentials, ssl=False)
        return pika.BlockingConnection(parameters)

