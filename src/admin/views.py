from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from src.core.schemas import (
    ResponseAccessToken
)
from src.admin.service import Service
from src.core.authorization import Authorization
from src.admin.schemas import (
    MasterInfoWithPassword, MasterInfoWithIdSchema, MasterUpdateSchema,
    MasterInfoSchema, RepairOrderSchema
)
from src.master.service import Servise as MasterService
from src.master.schemas import QuickInfoRepairOrderSchema
from src.admin.admin_auth import is_admin


router = APIRouter(
    prefix="/admin",
)


@router.post(
    "/auth",
    response_model=ResponseAccessToken,
)
def authorize_admin(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        service=Depends(Service),
        authorization=Depends(Authorization),
):
    """
    Authorization of the admin and issuance of an access token and refresh
    token.
    """
    is_valid = service.is_valid_admin_conf(
        form_data.username,
        form_data.password
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = authorization.create_access_token(
        data={"sub": form_data.username}
    )
    refresh_token = authorization.create_refresh_token(
        data={"sub": form_data.username}
    )

    response.set_cookie(
        "refresh_token",
        value=refresh_token,
        httponly=True
    )

    return ResponseAccessToken(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/auth/refresh",
    response_model=ResponseAccessToken,
)
def authorize_admin(
        response: Response,
        refresh_token: Optional[str] = Cookie(None),
        authorization=Depends(Authorization),
        service=Depends(Service)
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    data = authorization.get_data_from_jwt(refresh_token)

    if not service.is_admin(data["sub"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    access_token = authorization.create_access_token(
        data={"sub": data["sub"]}
    )
    refresh_token = authorization.create_refresh_token(
        data={"sub": data["sub"]}
    )

    response.set_cookie(
        "refresh_token",
        value=refresh_token,
        httponly=True
    )

    return ResponseAccessToken(
        access_token=access_token,
        token_type="bearer"
    )


@router.get(
    "/logout",
)
def admin_logout(
        response: Response,
):
    response.delete_cookie("refresh_token")
    return {"status": "success"}


@router.post(
    "/master",
    response_model=MasterInfoWithPassword,
    dependencies=[Depends(is_admin), ],
)
def add_new_master(
        master: MasterInfoWithPassword,
        service=Depends(Service),
):
    success, detail = service.add_master(master)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return master


@router.get(
    "/master/all",
    response_model=list[MasterInfoWithIdSchema],
    dependencies=[Depends(is_admin), ],
)
def get_all_masters(
        service=Depends(Service),
):
    """
    Выдаёт всех мастеров, которые есть в базе данных.
    """
    return service.get_all_masters()


@router.get(
    "/master/{master_id}",
    response_model=MasterInfoWithIdSchema,
    dependencies=[Depends(is_admin), ],
)
def get_master_info(
        master_id: int,
        service=Depends(Service),
):
    """
    Выдаёт информацию о конкретном мастере.
    """

    master = service.get_master(master_id)
    if not master:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Master not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return master


@router.put(
    "/master/{master_id}",
    response_model=MasterInfoSchema,
    dependencies=[Depends(is_admin), ],
)
def update_master_info(
        master_id: int,
        master_info: MasterUpdateSchema,
        service=Depends(Service),
):
    """
    Обновление данных у мастера.
    """
    status_code, response = service.update_master(master_id, master_info)

    if status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_code,
            detail=response,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response


@router.delete(
    "/master/{master_id}",
    response_model=MasterInfoSchema,
    dependencies=[Depends(is_admin), ],
)
def delete_master_info(
        master_id: int,
        service=Depends(Service),
):
    """
    Удаление мастера.
    """
    status_code, response = service.delete_master(master_id)

    if status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status_code,
            detail=response,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return response


@router.get(
    "/repair_orders/all",
    response_model=list[QuickInfoRepairOrderSchema],
    dependencies=[Depends(is_admin), ],
)
def get_all_repair_orders(
        master_service: MasterService = Depends(MasterService)
):
    return master_service.get_all_repair_orders()


@router.get(
    "/repair_orders/{repair_order_id}",
    response_model=RepairOrderSchema,
    dependencies=[Depends(is_admin), ],
)
def get_repair_order(
        repair_order_id: int,
        master_service: MasterService = Depends(MasterService)
):
    return master_service.get_repair_order(repair_order_id)
