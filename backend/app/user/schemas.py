from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str | None
    username: str | None
    email: str | None
    phone: str | None
    email_verified: bool
    phone_verified: bool
    is_active: bool


class UserUpdate(BaseModel):
    name: str | None = None
    # Deliberately no email/phone here -- changing those should go through
    # a dedicated verification flow, not a plain profile update. Stub that
    # in later (Section 16/17 discussion: change phone requires OTP).
