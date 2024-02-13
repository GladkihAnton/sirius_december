from aio_pika import RobustChannel, RobustExchange


channel: RobustChannel
exchange_users: RobustExchange

def get_exchange_users() -> RobustExchange:
    global exchange_users

    return exchange_users


def get_channel() -> RobustChannel:
    global channel

    return channel
