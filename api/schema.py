from pydantic import BaseModel
from typing import Optional

class WebsiteBase(BaseModel):
    domain: Optional[str]
    ttfb: Optional[float] = None
    is_analyze: Optional[bool]
    cms: Optional[str] = None
    techno_used: Optional[str] = None
    web_hoster: Optional[str] = None
    country_of_web_hoster: Optional[str] = None

class WebsiteCreate(WebsiteBase):
    pass

class Website(WebsiteBase):
    id: int
    domain: Optional[str] = None
    ttfb: Optional[float] = None
    is_analyze: Optional[bool] = None
    cms: Optional[str] = None
    techno_used: Optional[str] = None
    web_hoster: Optional[str] = None
    country_of_web_hoster: Optional[str] = None

    class Config:
        orm_mode = True
