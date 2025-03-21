from pydantic import BaseModel, EmailStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class MemberCreate(BaseModel):
    name: str
    password: str
    re_password: str
    email: EmailStr

    @field_validator('name', 'password', 're_password', 'email')
    def not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError("빈값은 허용하지 않습니다.")
        return value

    @field_validator('re_password')
    def password_match(cls, value, info: FieldValidationInfo):
        if 'password' in info.data and value != info.data['password']:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return value
