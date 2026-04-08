from pydantic import BaseModel, Field, EmailStr

class ContactInfoModel(BaseModel):
    email : EmailStr | None = Field(
        min_length=8,
        max_length=25,
        description="User's email"
        )
    phone_number : str | None = Field(
        min_length=10,
        max_length=10,
        pattern=r'^\d+$',
        description="User's phone number"
        )
    
class UserModel(BaseModel):
    first_name : str = Field(
        min_length=3,
        max_length=15,
        pattern=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$',
        description="User's first name"
        )
    middle_name : str = Field(
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
    middle_surname : str = Field(
        min_length=3,
        max_length=17,
        pattern=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ]+$',
        description="User's middle surname"
    )
    contac_info : ContactInfoModel = Field(description="User's contact info")