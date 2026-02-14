from pydantic import BaseModel,EmailStr
from typing import Optional
from .models import StatusChoices
from datetime import date,datetime

class UserProfileInputSchema(BaseModel):
    first_name: str
    last_name:str
    user_name:str
    email:EmailStr
    password:str
    age: Optional[int]
    phone_number: Optional[str]



class UserLoginSchema(BaseModel):
    user_name:str
    password:str


class UserProfileOutSchema(BaseModel):
    id: int
    first_name: str
    last_name:str
    user_name:str
    email:EmailStr
    age: Optional[int]
    phone_number: Optional[str]
    status: StatusChoices
    date_registered:date

class CategoryInputSchema(BaseModel):
    category_image:str
    category_name:str

class CategoryOutSchema(BaseModel):
    id: int
    category_image:str
    category_name:str


class SubCategoryInputSchema(BaseModel):
    sub_category_name:str
    category_id:int


class SubCategoryOutSchema(BaseModel):
    id:int
    sub_category_name:str
    category_id:int


class ProductInputShema(BaseModel):
    sub_category_id:int
    product_name:str
    price:int
    article_number:int
    created_date:date
    description: str
    video: str
    product_type: bool

class ProductOutShema(BaseModel):
    id: int
    sub_category_id:int
    product_name:str
    price:int
    article_number:int
    description:str
    video:str
    product_type: bool
    created_date:date



class ProductInputImageShema(BaseModel):
    image:str
    product_id:int

class ProductOutImageShema(BaseModel):
    id:int
    image:str
    product_id:int

class ReviewInputShema(BaseModel):
    product_id:int
    user_id: int
    stars:int
    created_date:datetime
    text: str

class ReviewOutShema(BaseModel):
    id:int
    user_id:int
    product_id:int
    text:str
    stars:int
    created_date:datetime






