# user model
# one-to-many with Post and Comment
# пользователь может иметь много сообщений и комментариев

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)

    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')
