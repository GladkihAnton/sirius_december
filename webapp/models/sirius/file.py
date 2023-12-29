from typing import List, TYPE_CHECKING

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.meta import DEFAULT_SCHEMA, Base

if TYPE_CHECKING:
    from webapp.models.sirius.user import User


class File(Base):
    __tablename__ = 'file'
    __table_args__ = ({'schema': DEFAULT_SCHEMA},)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    url: Mapped[str] = mapped_column(Text)
    task_id: Mapped[str] = mapped_column(String)

    users: Mapped[List['User']] = relationship(
        'User',
        secondary=f'{DEFAULT_SCHEMA}.user_file',
        back_populates='files',
    )
