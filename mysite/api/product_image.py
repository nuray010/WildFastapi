from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import ProductImage
from mysite.database.schema import ProductInputImageShema,ProductOutImageShema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

product_image_router = APIRouter(prefix='/product_image',tags=['product_image'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_image_router.post('/',response_model=ProductOutImageShema)
async def create_product_image(product_image: ProductInputImageShema,db: Session = Depends(get_db)):
    product_image_db = ProductImage(**product_image.dict())
    db.add(product_image_db)
    db.commit()
    db.refresh(product_image_db)
    return product_image_db


@product_image_router.get('/',response_model=List[ProductOutImageShema])
async def list_product_image(db: Session = Depends(get_db)):
     return db.query(ProductImage).all()

@product_image_router.get('/{product_image.id}/',response_model=ProductOutImageShema)
async def detail_product_image(product_image_id: int,db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id==product_image_id).first()
    if not product_image_db:
        raise HTTPException(detail='Here is no id like that',status_code=400)

    return product_image_db


@product_image_router.put('/{product_image_id}/', response_model=dict)
async def product_image_update(product_image_id: int, product_image: ProductInputImageShema, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id==product_image_id).first()
    if not product_image_db:
        raise HTTPException(detail='here is no like that information', status_code=400)

    for product_image_key, product_image_value in product_image.dict().items():
        setattr(product_image_db, product_image_key, product_image_value)


    db.commit()
    db.refresh(product_image_db)
    return {'message': 'information if changed'}


@product_image_router.delete('/{product_image_id}/', response_model=dict)
async def product_image_delete(product_image_id: int, db: Session = Depends(get_db)):
    product_image_db = db.query(ProductImage).filter(ProductImage.id==product_image_id).first()
    if not product_image_db:
        raise HTTPException(detail='here is no like that information', status_code=400)

    db.delete(product_image_db)
    db.commit()
    return {'massage': 'information is deleted'}
