from pydantic import BaseModel

from webapp.models.sirius.user_product_feedback import StatusFeedback


class PostFeedBackModel(BaseModel):
    product_id: int

    status: StatusFeedback
