

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from domain.member.schema import MemberCreate, MemberLoginPassword
from domain.member import service
from database import get_db  # DB 연결 의존성 주입

router = APIRouter(
    prefix="/member",
    tags=["member"]
)

@router.post("/register")
def register_member(
        member_create: MemberCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):

    service.create_member(db, member_create, background_tasks)
    return {"data":"이메일을 확인해주세요"}


@router.post("/login")
def login_with_password(
        member_login_password: MemberLoginPassword,
        db: Session = Depends(get_db)
):

    return service.login_with_password(db, member_login_password)



