from typing import List

from fastapi import Depends, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.utils import AppModel
from . import router

class ObjectResponse(AppModel):
    _id: str
    type:str
    price: int
    address:str
    area:float
    rooms_count:int
class GenResponse(AppModel):
    total:int
    objects:List[ObjectResponse]
    
@router.get("/shanyrak/review", response_model=GenResponse)
def shanyrak_review_for_moderator(
    limit:int,
    offset:int,
    jwt_data:JWTData=Depends(parse_jwt_user_data),
    svc:Service=Depends(get_service)
):
    if jwt_data.role != "moderator":
        raise HTTPException(status_code=403, detail="You are not moderator sorry!!!")
    val = svc.repository.review_houses(limit, offset)
    return GenResponse(**val)