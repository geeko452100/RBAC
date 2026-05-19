from pydantic import BaseModel

# Blueprint for the JWT auth token
class Token(BaseModel):
    access_token: str
    token_type: str 

# Blueprint to define the token's id for the user
class TokenData(BaseModel):
    user_id: int | None = None