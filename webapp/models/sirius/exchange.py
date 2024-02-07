from sqlalchemy import Integer, Column, ForeignKey
from webapp.models.meta import DEFAULT_SCHEMA, Base


class Exchange(Base):
    __tablename__ = 'exchange'
    __table_args__ = {'schema': DEFAULT_SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    item1_id = Column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.item.id"))
    item2_id = Column(Integer, ForeignKey(f"{DEFAULT_SCHEMA}.item.id"))