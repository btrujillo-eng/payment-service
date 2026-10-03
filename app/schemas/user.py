from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

Email = Annotated[EmailStr , Field(min_length=8, max_length=25, description="User's email")]

PhoneNumber = Annotated[str, Field(min_length=10, max_length=10, pattern=r'^\d+$', description="User's phone number")]

class BaseContactInfo(BaseModel):
    email : Email | None = None
    phone_number : PhoneNumber | None = None
    
class BaseUserData(BaseModel):
    first_name : str = Field(
        min_length=3,
        max_length=15,
        pattern=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$',
        description="User's first name"
    )
    middle_name : str | None = Field(
        default=None,
        min_length=3,
        max_length=15,
        pattern=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$',
        description="User's middle name"
    )
    first_surname : str = Field(
        min_length=3,
        max_length=17,
        pattern=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$',
        description="User's first surname"
    )
    middle_surname : str | None = Field(
        default=None,
        min_length=3,
        max_length=17,
        pattern=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$',
        description="User's middle surname"
    )
    contact_info : BaseContactInfo = Field(description="User's contact info")