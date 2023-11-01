from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from src.core.schemas import (
    ResponseTokens, ResponseAccessToken, RequestRefreshToken
)
from src.master.model import MasterModel
from typing import Annotated
from src.master.service import Servise
from src.core.authorization import Authorization
from starlette import status

router = APIRouter(
    prefix='/master',
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='master/auth')


@router.post(
    '/login',
    response_model=ResponseTokens,
)
def authorize_master(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        servise=Depends(Servise),
        authorization=Depends(Authorization),
):
    """
       Authorization of the master and issuance of an access token and refresh
       token.
       """
    response_code, response = servise.get_master(form_data.username, form_data.password)
    if response_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=response_code,
            detail=response,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = authorization.create_access_token(
        data={"sub": form_data.username}
    )
    refresh_token = authorization.create_refresh_token(
        data={"sub": form_data.username}
    )

    return ResponseTokens(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )