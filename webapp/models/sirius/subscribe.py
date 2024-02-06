import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.user.id'), primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, ForeignKey(f'{DEFAULT_SCHEMA}.course.id'), primary_key=True)
    subscription_date: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='subscriptions')
    course = relationship('Course', back_populates='subscriptions')
