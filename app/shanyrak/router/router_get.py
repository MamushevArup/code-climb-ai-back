from pydantic import Field
from typing import Any

from fastapi import Depends

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.utils import AppModel
from . import router


class GetPostResponse(AppModel):
    id : Any = Field(alias="_id")
    type : str
    price : int
    address : str
    area : float
    rooms_count : int
    description : str
    user_id: Any
    media : list | None
    location : dict | None

@router.get("/shanyraks/{id:str}", response_model=GetPostResponse)
def get_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    model = svc.repository.get_shanyrak_by_id(shanyrak_id, "shanyraq")
    return GetPostResponse(**model)