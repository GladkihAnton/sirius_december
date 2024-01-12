from typing import Any, Dict, List

# simulates sending messages to Kafka and appending the sent messages to a list for testing purposes
class TestKafkaProducer:
    def __init__(self, kafka_received_messages: List[Dict[str, Any]]):
        self.kafka_received_messages: List[
            Dict[str, Any]
        ] = kafka_received_messages
    
    async def send_and_wait(
        self,
        topic,
        value=None,
        key=None,
        partition=None,
        timestamp_ms=None,
        headers=None,
    ):
        self.kafka_received_messages.append(
            {
                'topic': topic,
                'value': value,
                'partition': partition,
            }
        )


# класс TestKafkaProducer для мокирования Kafka Producer.

# Класс имеет метод __init__, который инициализирует список kafka_received_messages
# для хранения полученных сообщений Kafka.

# Метод send_and_wait используется для отправки сообщения в Kafka и добавления
# информации о сообщении в список kafka_received_messages.

# Параметры метода send_and_wait соответствуют параметрам метода send в Kafka
# Producer. Однако, в этом случае, вместо отправки сообщения в Kafka, метод добавляет
# информацию о сообщении в список kafka_received_messages.

# Таким образом, этот класс может использоваться для тестирования приложений, которые
# используют Kafka Producer, без необходимости подключения к реальному Kafka брокеру.
# Вместо этого, можно использовать экземпляр этого класса для мокирования Kafka
# Producer и проверки корректности отправки сообщений.


# Для проверки работы Kafka можно использовать несколько подходов:

# 1. Запустить Kafka Consumer и прослушивать топик, в который
# отправляются сообщения. Это позволит убедиться, что сообщения
# успешно отправляются в Kafka и могут быть получены.

# 2. Использовать Kafka Tool или другой инструмент для мониторинга Kafka, чтобы
# проверить состояние брокеров, топиков и групп потребителей. Это поможет убедиться,
# что Kafka работает корректно и все компоненты функционируют без ошибок.

# 3. Написать тесты для приложения, которое использует Kafka Producer и/или Consumer.
# Тесты могут проверять отправку и получение сообщений, обработку ошибок, работу с
# разными топиками и группами потребителей и т.д.

# 4. Использовать инструменты для нагрузочного тестирования, такие как
# Apache JMeter или Gatling, чтобы проверить производительность Kafka
# при обработке большого количества сообщений.

# 5. Мониторить логи Kafka и приложений, использующих Kafka, чтобы быстро выявлять
# проблемы и ошибки в работе системы.
