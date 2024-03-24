from aio_pika import ExchangeType, connect_robust

from webapp.db import rabbitmq


async def start_rabbit():
    connection = await connect_robust('amqp://rmuser:rmpassword@rabbitmq/')
    rabbitmq.channel = await connection.channel(publisher_confirms=False)

    rabbitmq.exchange_users = await rabbitmq.channel.declare_exchange('users', ExchangeType.FANOUT)
    rabbitmq.exchange_orders = await rabbitmq.channel.declare_exchange('orders', ExchangeType.DIRECT)

    queue = await rabbitmq.channel.declare_queue('orders', auto_delete=False, durable=True)

    await queue.bind(rabbitmq.exchange_orders, 'orders')
