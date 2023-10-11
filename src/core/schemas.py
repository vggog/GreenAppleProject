from pydantic import BaseModel


class ResponseAccessToken(BaseModel):
    access_token: str
    token_type: str


class ResponseTokens(ResponseAccessToken):
    refresh_token: str


class RequestRefreshToken(BaseModel):
    refresh_token: str
