#schemas is where validation takes place at the router level
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field,ConfigDict,field_validator,EmailStr,model_validator
from models.employee import EmployeeRole
class AddressCreate(BaseModel):
    line1: str
    city:str
    postalcode: str
    country:str

    @field_validator("postalcode")

    @classmethod
    def validate_postal_code(cls,v:str) ->str:
        if not v.isdigit():
            raise ValueError("Postal code must contain only digits (0-9)")
        return v
    
    @model_validator(mode="after")

    def postal_code_length_for_country(self):

        country = self.country.strip().upper()

        n = len(self.postalcode)

        if country in ("US", "USA") and n != 5:

            raise ValueError("US ZIP codes must be exactly 5 digits")

        elif country == "IN" and n != 6:

            raise ValueError("Indian PIN codes must be exactly 6 digits")

        return self


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True,extra="forbid")
    name:str
    email:EmailStr
    age: int |None =Field(ge=10,le=100)
    password: str = Field(min_length=6)
    role:EmployeeRole
    address: AddressCreate |None = None




class EmployeeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
    id:    int
    name:  str
    email: str
    age:   int | None = None
    addresses: list[AddressCreate] = []

class EmployeeResponseId(EmployeeResponse):
    created_at: datetime
    updated_at:datetime


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None