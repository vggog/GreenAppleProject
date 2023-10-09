from pydantic import BaseModel


class ResponseTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
