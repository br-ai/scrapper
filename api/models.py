from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float

# from .database import Base
from database import Base

class Website(Base):
    __tablename__ = "website"
    id = Column(Integer,primary_key=True,index=True)
    domain = Column(String(255),index=True)
    ttfb = Column(Float)
    is_analyze = Column(Boolean,default=False)