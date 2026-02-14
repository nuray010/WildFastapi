from fastapi import HTTPException,APIRouter,Depends
from sqlalchemy.testing.pickleable import User
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile,RefreshToken
from mysite.database.schema import UserProfileInputSchema,UserProfileOutSchema,UserLoginSchema
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from mysite.config import (SECRET_KEY,REFRESH_TOKEN_LIFETIME,ALGORITHM,ACCESS_TOKEN_LIFETIME)
from datetime import datetime, timedelta,timezone
from jose import jwt
from typing import Optional


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router =OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(prefix="/auth",tags=["auth"])
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_LIFETIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def create_refresh_token(data: dict):
   return create_access_token(data,expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post("/register",response_model=dict)
async def register(user: UserProfileInputSchema,db:Session = Depends(get_db)):
   user_db = db.query(UserProfile).filter(UserProfile.user_name == user.user_name).first()
   email_db = db.query(UserProfile).filter(UserProfile.email == user.email).first()
   if user_db or email_db:
    raise HTTPException(detail='Like this username  or email already exist',status_code=400)

   hash_password = get_password_hash(user.password)
   user_data = UserProfile(
        first_name=user.first_name,
       last_name=user.last_name,
       user_name=user.user_name,
       email=user.email,
       age=user.age,
       phone_number =user.phone_number,
       password = hash_password,
    )
   db.add(user_data)
   db.commit()
   db.refresh(user_data)
   return {'message':'You are registered successfully!'}



@auth_router.post("/login",response_model=dict)
async def login(user:UserLoginSchema,db:Session = Depends(get_db)):
    username_db = db.query(UserProfile).filter(UserProfile.user_name == user.user_name).first()
    if not username_db or not verify_password(user.password,username_db.password):
        raise HTTPException(status_code=400,detail="Incorrect username")


    access_token =  create_access_token({'sub':username_db.user_name})
    refresh_token = create_refresh_token({'sub': username_db.user_name})

    token_db = RefreshToken(user_id=username_db.id,token=refresh_token)
    db.add(token_db)
    db.commit()


    return {'access_token': access_token,'refresh_token': refresh_token,'token_type': 'bearer'}



@auth_router.post("/logout")
async def logout(refresh_token:str,db:Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    if not stored_token:
        raise HTTPException(status_code=400,detail="Incorrect refresh token")

    db.delete(stored_token)
    db.commit()

    return {'message':'You have been logged out!'}


@auth_router.post('/refresh')
async def refresh(refresh_token:str,db:Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
    if not stored_token:
        raise HTTPException(status_code=400, detail="Incorrect refresh token")

    access_token = create_access_token({'sub': stored_token.id})

    return {'access_token': access_token,'token_type': 'bearer'}




