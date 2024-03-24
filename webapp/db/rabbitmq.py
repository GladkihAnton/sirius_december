from aio_pika import RobustChannel, RobustExchange

channel: RobustChannel
exchange_users: RobustExchange
exchange_orders: RobustExchange

def get_exchange_orders() -> RobustExchange:
    global exchange_orders

    return exchange_orders


def get_exchange_users() -> RobustExchange:
    global exchange_users

    return exchange_users


def get_channel() -> RobustChannel:
    global channel

    return channel
