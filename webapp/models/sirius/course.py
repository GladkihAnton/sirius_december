from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class Course(Base):
    __tablename__ = 'course'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String)
    difficulty: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    lessons = relationship('Lesson', back_populates='course', cascade='all, delete-orphan')
    subscriptions = relationship('Subscription', back_populates='course', cascade='all, delete-orphan')
