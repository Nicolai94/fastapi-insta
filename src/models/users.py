from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.db.database import Base


class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("DBArticle", back_populates="user")
