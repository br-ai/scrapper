"""
main file for executing api functions and routes
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import models
import schema
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    """
    Get the local session of database
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/websites/",response_model=schema.Website)
def post_website(website:schema.WebsiteCreate, db:Session=Depends(get_db)):
    return crud.create_website(db=db,website=website)


@app.get("/websites/", response_model=list[schema.Website])
def get_websites(skip:int=0, limit:int=0, db:Session=Depends(get_db)):
    return crud.get_websites(db,skip=skip,limit=limit)

@app.get("/websites/{id}",response_model=schema.Website)
def get_website(id:int, db:Session=Depends(get_db)):
    website = crud.get_website(db,id=id)
    if website is None:
        raise HTTPException(status_code=404, detail=f"website: '{website}' not found")
    return website

@app.get("/unscrapped_websites/", response_model=list[schema.Website])
def get_unscrapped_websites(skip:int=0, limit:int=0, db:Session=Depends(get_db)):
    return crud.get_unscrapped_websites(db,skip=skip,limit=limit)

@app.patch("/websites/{domain}", response_model=schema.Website)
def patch_website(domain: str, website_update: schema.WebsiteUpdate, db: Session = Depends(get_db)):
    updated_website = crud.update_website(db=db, domain=domain, website_update=website_update)
    if updated_website is None:
        raise HTTPException(status_code=404, detail=f"Website with domain '{domain}' not found")
    return updated_website