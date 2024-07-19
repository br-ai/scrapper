from pydantic import BaseModel

class WebsiteBase(BaseModel):
    domain: str
    ttfb: float
    is_analyze: bool

class WebsiteCreate(WebsiteBase):
    pass 

class Website(WebsiteBase):
    id : int
    domain : str
    ttfb : float
    is_analyze : bool

    class Config:
        orm_model = True
