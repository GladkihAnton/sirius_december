from sqlalchemy import Integer, String, Column
from webapp.models.meta import DEFAULT_SCHEMA, Base


class Item(Base):
    __tablename__ = 'item'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
