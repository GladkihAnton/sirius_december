from pathlib import Path

import msgpack

BASE_DIR = Path(__file__).parent

WIDTH = 123
HEIGHT = 123
MOCKED_HEX = 'mocked_hex'

with open(BASE_DIR / 'test_file', 'rb') as file:
    image = file.read()


value = msgpack.packb(
    {
        'image': image,
        'task_id': MOCKED_HEX,
        'width': WIDTH,
        'height': HEIGHT,
    }
)
