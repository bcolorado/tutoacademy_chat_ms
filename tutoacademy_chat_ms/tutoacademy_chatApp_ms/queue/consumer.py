import json
import pika
#from tutoacademy_chatApp_ms.views.chat_view import *
import requests

rabbit_settings = {
    "protocol": "amqp",
    "hostname": "10.64.1.158",
    "port": 5672,
    "username": "guest",
    "password": "guest",
    "vhost": "/",
    "auth_mechanism": ["PLAIN", "AMQPLAIN", "EXTERNAL"]
}


credentials = pika.PlainCredentials(rabbit_settings['username'], rabbit_settings['password'])
parameters = pika.ConnectionParameters(
    host=rabbit_settings['hostname'],
    port=rabbit_settings['port'],
    virtual_host=rabbit_settings['vhost'],
    credentials=credentials,
    connection_attempts=5,
    retry_delay=5,
    socket_timeout=10
)




def connect_consume():
    value=None
    queue = "queries"
    try:

        with pika.BlockingConnection(parameters) as connection:
            channel = connection.channel()

            res = channel.queue_declare(queue=queue, durable=False)

            def on_message(channel, method, properties, body):
                query = json.loads(body)
                value=query
                print("Received msg:",str(query))
                requests.patch('http://0.0.0.0:8000/chat/', json=query)  #IMPORTANT, change the URL 

                channel.basic_ack(delivery_tag=method.delivery_tag)
                print("Deleted message from queue")

            channel.basic_consume(queue, on_message)

            print("Consumer is working!")
            channel.start_consuming()
        return value
    except Exception as e:
        print("Consumer failed!")
        print(str(e))

#connect_consume()


