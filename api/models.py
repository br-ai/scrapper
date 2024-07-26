from sqlalchemy import Boolean, Column, Integer, String, Float

# from .database import Base
from database import Base

class Website(Base):
    __tablename__ = "website"
    id = Column(Integer,primary_key=True, index=True)
    domain = Column(String(255), index=True)
    ttfb = Column(Float, nullable=True)
    is_analyze = Column(Boolean, default=False)
    cms = Column(String(255), index=True, nullable=True)
    techno_used = Column(String(255), index=True, nullable=True)
    web_hoster = Column(String(255), index=True, nullable=True)
    country_of_web_hoster = Column(String(255), index=True, nullable=True)