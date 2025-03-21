from sqlalchemy import Column, Integer, String

from database import Base

class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    code = Column(String, nullable=False)
