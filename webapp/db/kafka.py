import random
from typing import List

from aiokafka.producer import AIOKafkaProducer

producer: AIOKafkaProducer
partitions: List[int]


def get_producer() -> AIOKafkaProducer:
    global producer

    return producer


def get_partition() -> int:
    global partitions

    return random.choice(partitions)
