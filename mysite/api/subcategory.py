from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import SubCategory
from mysite.database.schema import SubCategoryInputSchema,SubCategoryOutSchema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

sub_category_router = APIRouter(prefix='/subcategory', tags=['subcategory'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@sub_category_router.post('/',response_model=SubCategoryOutSchema)
async def create_subcategory(sub_category:SubCategoryInputSchema,db: Session = Depends(get_db)):
    sub_category_db = SubCategory(**sub_category.dict())
    db.add(sub_category_db)
    db.commit()
    db.refresh(sub_category_db)
    return sub_category_db


@sub_category_router.get('/',response_model=List[SubCategoryOutSchema])
async def list_subcategory(db: Session = Depends(get_db)):
     return db.query(SubCategory).all()

@sub_category_router.get('/{sub_category.id}/',response_model=SubCategoryOutSchema)
async def detail_review(subcategory_id: int,db: Session = Depends(get_db)):
    subcategory_db = db.query(SubCategory).filter(SubCategory.id==subcategory_id).first()
    if not subcategory_db:
        raise HTTPException(detail='Here is no id like that',status_code=400)

    return subcategory_db



@sub_category_router.put('/{sub_category_id}/', response_model=dict)
async def sub_category_update(sub_category_id: int, sub_category: SubCategoryInputSchema, db: Session = Depends(get_db)):
    sub_category_db = db.query(SubCategory).filter(SubCategory.id==sub_category_id).first()
    if not sub_category_db:
        raise HTTPException(detail='Here is no message like that', status_code=400)

    for sub_category_key, sub_category_value in sub_category.dict().items():
        setattr(sub_category_db, sub_category_key, sub_category_value)


    db.commit()
    db.refresh(sub_category_db)
    return {'message': 'Message changed'}


@sub_category_router.delete('/{sub_category_id}/', response_model=dict)
async def sub_category_delete(sub_category_id: int, db: Session = Depends(get_db)):
    sub_category_db = db.query(SubCategory).filter(SubCategory.id==sub_category_id).first()
    if not sub_category_db:
        raise HTTPException(detail='Here is no message like that', status_code=400)

    db.delete(sub_category_db)
    db.commit()
    return {'massage': 'Message is deleted'}