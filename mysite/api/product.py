from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import Product
from mysite.database.schema import ProductOutShema,ProductInputShema
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
from typing import List

product_router = APIRouter(prefix='/product', tags=['product'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@product_router.post('/',response_model=ProductOutShema)
async def create_product(product: ProductInputShema,db: Session = Depends(get_db)):
    product_db = Product(**product.dict())
    db.add(product_db)
    db.commit()
    db.refresh(product_db)
    return product_db


@product_router.get('/',response_model=List[ProductOutShema])
async def list_product(db: Session = Depends(get_db)):
     return db.query(Product).all()

@product_router.get('/{product.id}/',response_model=ProductOutShema)
async def detail_product(product_id: int,db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()
    if not product_db:
        raise HTTPException(detail='Here is no id like that',status_code=400)

    return product_db



@product_router.put('/{product_id}/', response_model=dict)
async def product_update(product_id: int, product: ProductInputShema, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()
    if not product_db:
        raise HTTPException(detail='here is no information like that', status_code=400)

    for product_key, product_value in product.dict().items():
        setattr(product_db, product_key, product_value)


    db.commit()
    db.refresh(product_db)
    return {'message': 'Information is changed'}


@product_router.delete('/{product_id}/', response_model=dict)
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    product_db = db.query(Product).filter(Product.id==product_id).first()
    if not product_db:
        raise HTTPException(detail='Мындай маалымат жок', status_code=400)

    db.delete(product_db)
    db.commit()
    return {'massage': 'Here is no information like that'}