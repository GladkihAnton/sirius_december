from webapp.cache.rabbit.key_builder import get_user_products_queue_key
from webapp.db.rabbitmq import get_channel, get_exchange_users


async def declare_queue(user_id: int) -> None:
    channel = get_channel()

    queue_key = get_user_products_queue_key(user_id)

    exchange_users = get_exchange_users()
    queue = await channel.declare_queue(queue_key, auto_delete=False, durable=True)

    await queue.bind(exchange_users, queue_key)
