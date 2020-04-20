mq_config = {
    'host': "localhost",
    'port': "5672",
    'userName': "guest",
    'password': "guest",
    'virtualHost': "/"
}

image_process_request_config = {

    'exchangeName': "image_process_request_exchange",
    'exchangeType': "topic",
    'exchangeOptions': {
        'passive': False,
        'durable': True,
        'autoDelete': False,
        'internal': False
    },
    'routingKey': "*.*.*",
    'queueName': "image_process_request_queue",
    'queueOptions': {
        'passive': False,
        'durable': True,
        'exclusive': False,
        'autoDelete': False,
    },
}

