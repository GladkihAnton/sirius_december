from typing import Any, Dict, List


class TestKafkaProducer:
    def __init__(self, kafka_received_messages: List[Dict[str, Any]]):
        self.kafka_received_messages: List[Dict[str, Any]] = kafka_received_messages

    async def send_and_wait(self, topic, value=None, key=None, partition=None, timestamp_ms=None, headers=None):
        self.kafka_received_messages.append(
            {
                'topic': topic,
                'value': value,
                'partition': partition,
            }
        )
