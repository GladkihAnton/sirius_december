from datetime import datetime

from pydantic import BaseModel


class Subscription(BaseModel):
    user_id: int
    course_id: int
    subscription_date: datetime

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'user_id': 1,
                    'course_id': 1,
                }
            ]
        }
    }
