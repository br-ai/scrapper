from sqlalchemy.orm import Session

# from . import models,schema
import models
import schema


def get_website(db: Session, website_id: int):
    return db.query(models.Website).filter(models.Website.id == website_id).first()


def get_websites(db: Session, skip:int=0, limit:int=100):
    return db.query(models.Website).offset(skip).limit(limit).all()

def get_website_by_domain(db: Session, domain: str):
    return db.query(models.Website).filter(models.Website.domain == domain).first()

def create_website(db: Session, website:schema.WebsiteCreate):
    db_website = models.Website(domain=website.domain, is_analyze=False)
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website

def get_unscrapped_websites(db: Session, skip:int=0, limit:int=100):
    return db.query(models.Website).filter(models.Website.is_analyze == False)

def update_website(db: Session, domain: str, website_update: schema.WebsiteUpdate):
    db_website = get_website_by_domain(db, domain=domain)
    if db_website is None:
        return None
    update_data = website_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_website, key, value)
    db.commit()
    db.refresh(db_website)
    return db_website