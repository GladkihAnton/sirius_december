from aio_pika import ExchangeType, connect_robust

from webapp.db import rabbitmq


async def start_rabbit():
    connection = await connect_robust('amqp://rmuser:rmpassword@rabbitmq/')
    rabbitmq.channel = await connection.channel(publisher_confirms=False)

    rabbitmq.exchange_users = await rabbitmq.channel.declare_exchange('users', ExchangeType.FANOUT)

    # connection = await connect_robust(
    #     "amqp://rmuser:rmpassword@rabbitmq/",
    # )
    #
    # queue_name = "test_queue12"
    # routing_key = "test_queue12w9i tm "
    #
    # # Creating channel
    # channel = await connection.channel()
    #
    # # Declaring exchange
    # exchange = await channel.declare_exchange('test12', type=ExchangeType.FANOUT, auto_delete=False, durable=True)
    #
    # # Declaring queue
    # queue = await channel.declare_queue(queue_name, auto_delete=False, durable=True)
    # queue1 = await channel.declare_queue(queue_name + '1', auto_delete=False, durable=True)
    # queue2 = await channel.declare_queue(queue_name + '2', auto_delete=False, durable=True)
    #
    # # Binding queue
    # await queue.bind(exchange, routing_key)
    # await queue1.bind(exchange, routing_key + '1')
    # await queue2.bind(exchange, routing_key + '2')
    #
    # await exchange.publish(
    #     Message(
    #         bytes('Hello', 'utf-8'),
    #         content_type='text/plain',
    #         headers={'foo': 'bar'}
    #     ),
    #     routing_key
    # )
    #
    # # Receiving message
    # incoming_message = await queue.get(timeout=5)
    # print(incoming_message.body.decode())
    # incoming_message = await queue1.get(timeout=5)
    # print(incoming_message.body.decode())
    # incoming_message = await queue2.get(timeout=5)
    # print(incoming_message.body.decode())
    #
    # # Confirm message
    # await incoming_message.ack()
    #
    # await queue.unbind(exchange, routing_key)
    # await queue.delete()
    # await connection.close()
