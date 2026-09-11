from datetime import date

from pydantic import BaseModel, computed_field

from app.models.users import UserGenders, UserRoles

class CreateUser(BaseModel):
    email: str
    otp: str
    role: UserRoles
    date_of_birth: str
    first_name: str
    last_name: str
    display_name: str
    gender: UserGenders

    @computed_field
    @property
    def birthdate(self) -> date:
        return date.fromisoformat(self.date_of_birth)

class UpdateUser(BaseModel):
    pass

class ShowUser(BaseModel):
    pass