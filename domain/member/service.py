
from fastapi import BackgroundTasks, HTTPException
from starlette import status

from domain.member.schema import MemberCreate
from models import Member
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import random
from utils.mail import send_email_with_inline_qr
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_member(db:Session, member_create: MemberCreate, background_tasks: BackgroundTasks):

    if exists_by_email(db,member_create=member_create):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="이미 존재하는 사용자 입니다.")


    code = ''.join(random.choices('0123456789', k=10))
    member = Member(
        name=member_create.name,
        password=pwd_context.hash(member_create.password),
        email=str(member_create.email),
        code=code
    )
    db.add(member)
    db.commit()

    background_tasks.add_task(send_email_with_inline_qr,member.email,code)

def exists_by_email(db: Session, member_create :MemberCreate):
    return db.query(Member).filter(
        Member.email == member_create.email
    ).first()