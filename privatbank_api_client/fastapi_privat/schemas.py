from pydantic import BaseModel, Field


class PrivatSchema(BaseModel):
    privat_token: str = Field(..., max_length=292)
    privat_iban: str = Field(..., max_length=29)
    user_id: str

    class Config:
        from_attributes = True


class PrivatSchemaUpdate(BaseModel):
    privat_token: str = Field(..., max_length=292)
    privat_iban: str = Field(..., max_length=29)

    class Config:
        from_attributes = True


class PrivatSchemaPayment(BaseModel):
    amount: float = Field(..., ge=0.01)
    recipient: str = Field(..., max_length=16)
    user_id: str

    class Config:
        from_attributes = True
