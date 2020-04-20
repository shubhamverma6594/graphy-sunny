import pika
import functools
import threading
import logging
import time

class Consumer:
    def __init__(self, queue_config, mq_config):
        self.mq_config = mq_config
        self.config = queue_config
        self.connection = self._create_connection()

    def __enter__(self):
        self.connection = self._create_connection()
        return self

    def __exit__(self, *args):
        self.connection.close()

    def consume(self, message_received_callback):
        self.message_received_callback = message_received_callback

        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=25)

        self._create_exchange(channel)
        self._create_queue(channel)

        channel.queue_bind(queue=self.config['queueName'], exchange=self.config['exchangeName'], routing_key=self.config['routingKey'])

        channel.basic_consume(self._consume_message, queue=self.config['queueName'])

        t1 = threading.Thread(target=channel.start_consuming)
        t1.start()
        t1.join(0)

    def _create_exchange(self, channel):
        exchange_options = self.config['exchangeOptions']
        channel.exchange_declare(exchange=self.config['exchangeName'],
                                 exchange_type=self.config['exchangeType'],
                                 passive=exchange_options['passive'],
                                 durable=exchange_options['durable'],
                                 auto_delete=exchange_options['autoDelete'],
                                 internal=exchange_options['internal'])

    def _create_queue(self, channel):
        queue_options = self.config['queueOptions']
        channel.queue_declare(queue=self.config['queueName'],
                              passive=queue_options['passive'],
                              durable=queue_options['durable'],
                              exclusive=queue_options['exclusive'],
                              auto_delete=queue_options['autoDelete'])

    def _create_connection(self):
        credentials = pika.PlainCredentials(self.mq_config['userName'], self.mq_config['password'])
        parameters = pika.ConnectionParameters(self.mq_config['host'], self.mq_config['port'], self.mq_config['virtualHost'], credentials, ssl=False)
        return pika.BlockingConnection(parameters)
    def _consume_message(self, channel, method, properties, body):
        self.message_received_callback(body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
