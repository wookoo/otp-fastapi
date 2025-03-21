from fastapi import BackgroundTasks, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from datetime import timedelta, datetime

from starlette.config import Config

from domain.member.schema import MemberCreate, MemberLoginPassword
from models import Member
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import random
from utils.mail import send_email_with_inline_qr
from jose import jwt, JWTError

config = Config('.env')
ACCESS_TOKEN_EXPIRE_MINUTES = int(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_member(db: Session, member_create: MemberCreate, background_tasks: BackgroundTasks):
    if exists_by_email(db, email=str(member_create.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자 입니다.")

    code = ''.join(random.choices('0123456789', k=10))
    member = Member(
        name=member_create.name,
        password=pwd_context.hash(member_create.password),
        email=str(member_create.email),
        code=code
    )
    db.add(member)
    db.commit()

    background_tasks.add_task(send_email_with_inline_qr, member.email, code)


def exists_by_email(db: Session, email: str):
    return db.query(Member).filter(
        Member.email == email
    ).first()


def login_with_password(db: Session, member_login_password: MemberLoginPassword):
    member = exists_by_email(db,email=str(member_login_password.email))
    print(member.password)

    if not member or not pwd_context.verify(member_login_password.password,member.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="회원을 찾을 수 없습니다")

    data = {
        "sub": member.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
    }

