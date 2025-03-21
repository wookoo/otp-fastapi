from fastapi import BackgroundTasks

from domain.member.schema import MemberCreate
from models import Member
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import random
from utils.mail import send_email_with_inline_qr
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_member(db:Session, member_create: MemberCreate, background_tasks: BackgroundTasks):

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
