from sqlalchemy import Integer, String, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship

from src.db.database import Base


class DBArticle(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("DBUser", back_populates="items")
