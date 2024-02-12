import asyncio
from aio_pika import connect_robust, Message


async def start_rabbit():
    connection = await connect_robust(
        "amqp://rmuser:rmpassword@rabbitmq/",
    )

    queue_name = "test_queue"
    routing_key = "test_queue"

    # Creating channel
    channel = await connection.channel()

    # Declaring exchange
    exchange = await channel.declare_exchange('direct', auto_delete=False, durable=True)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, auto_delete=False, durable=True)
    
    # Binding queue
    await queue.bind(exchange, routing_key)

    await exchange.publish(
        Message(
            bytes('Hello', 'utf-8'),
            content_type='text/plain',
            headers={'foo': 'bar'}
        ),
        routing_key
    )

    # Receiving message
    incoming_message = await queue.get(timeout=5)
    print(incoming_message)

    # Confirm message
    await incoming_message.ack()

    await queue.unbind(exchange, routing_key)
    await queue.delete()
    await connection.close()
