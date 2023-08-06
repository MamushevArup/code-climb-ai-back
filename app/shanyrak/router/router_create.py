from datetime import datetime
from pydantic import Field
from typing import Any
from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreatePostRequest(AppModel):
    type : str
    price : int
    address : str
    area : float
    rooms_count : int
    description : str

class CreatePostResponse(AppModel):
    id : Any = Field(alias="_id")

@router.post("/shanyraks", response_model=CreatePostResponse)
def create_shanyrak(
    input: CreatePostRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    coord = svc.here_service.get_coordinates(input.address)
    json = {"location" : coord}
    shan_id = svc.repository.create_post_shanyraq(jwt_data.user_id, input.dict() | json | {"created_at" : datetime.utcnow()}, "waitlist")
    return CreatePostResponse(id=shan_id)