from pydantic import BaseModel

from webapp.models.sirius.user_product_feedback import StatusFeedbackEnum


class PostFeedBackModel(BaseModel):
    product_id: int

    status: StatusFeedbackEnum
