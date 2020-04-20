mq_config = {
    'host': "llama.rmq.cloudamqp.com",
    'port': "5672",
    'userName': "hcizhelk",
    'password': "odYzThGJnlFhHXl7NQ1wOA2G_3KQjXzg",
    'virtualHost': "hcizhelk"
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

