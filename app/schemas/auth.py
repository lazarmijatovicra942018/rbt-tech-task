from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(description="User's login name")
    password: str = Field(description="User's password")