from sqlalchemy.orm import Session

# from . import models,schema
import models
import schema


def get_website(db: Session, website_id: int):
    return db.query(models.Website).filter(models.Website.id == website_id).first()


def get_websites(db: Session, skip:int=0, limit:int=100):
    return db.query(models.Website).offset(skip).limit(limit).all()

def create_website(db: Session, website:schema.WebsiteCreate):
    db_website = models.Website(domain=website.domain, is_analyze=False)
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website

def get_unscrapped_websites(db: Session, skip:int=0, limit:int=100):
    return db.query(models.Website).filter(models.Website.is_analyze == False)