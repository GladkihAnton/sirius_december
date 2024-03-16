from webapp.models.sirius.order import Order


async def handle_order(order: Order) -> None:
    ...
    # TODO класть в очередь заказы
    # достаем из очереди по запросу из бота.
    # запрос из бота путем нажатия кнопки у доставщика
    # если очередь пуста, то делаем полинг или ws
