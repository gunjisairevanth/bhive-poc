from pydantic import BaseModel, Field
import uuid
# Pydantic model for creating a user
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)

    class Config:
        orm_mode = True
        on_encoders = {
            uuid.UUID: lambda v: str(v)
        }

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class ListFunds(BaseModel):
    Scheme_Code: int
    Date: str
    ISIN_Div_Payout_ISIN_Growth: str
    ISIN_Div_Reinvestment: str
    Mutual_Fund_Family: str
    Net_Asset_Value: float
    Scheme_Category: str
    Scheme_Name: str
    Scheme_Type: str

class ListFundsQuery(BaseModel):
    Scheme_Code: int
    Date: str
    ISIN_Div_Payout_ISIN_Growth: str
    ISIN_Div_Reinvestment: str
    Mutual_Fund_Family: str
    Net_Asset_Value: float
    Scheme_Category: str
    Scheme_Name: str
    Scheme_Type: str