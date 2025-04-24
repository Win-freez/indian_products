import re

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'",
                              examples=['+79005003030'])
    first_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[А-Яа-яA-Za-z\-]+$",
                            description="Имя, от 2 до 50 символов", examples=['Иван'])
    last_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[А-Яа-яA-Za-z\-]+$",
                           description="Фамилия, от 2 до 50 символов", examples=['Смирнов'])

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\+\d{5,15}$', value):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 5 до 15 цифр')
        return value

    model_config = ConfigDict(from_attributes=True)

class UserAuthSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")

    model_config = ConfigDict(from_attributes=True)

class UserOutSchema(BaseModel):
    id: int = Field(..., gt=0, description='User ID')
    email: EmailStr = Field(..., description="Электронная почта")
    phone_number: str = Field(..., description="Номер телефона в международном формате, начинающийся с '+'",
                              examples=['+79005003030'])
    first_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[А-Яа-яA-Za-z\-]+$",
                            description="Имя, от 2 до 50 символов", examples=['Иван'])
    last_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[А-Яа-яA-Za-z\-]+$",
                           description="Фамилия, от 2 до 50 символов", examples=['Смирнов'])

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'