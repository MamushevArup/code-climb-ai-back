from typing import List, Optional

from fastapi import Depends
from ..service import Service, get_service
from app.utils import AppModel
from . import router

class InsideObjectResponse(AppModel):
    _id:str
    address:str
    type:str
    price:int
    area:float
    rooms_count:int
    location:dict

class GenResponse(AppModel):
    total:int
    objects: List[InsideObjectResponse]

@router.get("/shanyraks")
def get_shanyraks(
    limit:int,
    offset:int,
    type:Optional[str]=None,
    rooms_count:Optional[int]=None,
    price_from:Optional[int]=None,
    price_until:Optional[int]=None,
    svc : Service = Depends(get_service)
):
    val = svc.repository.pagination(limit, offset, type, rooms_count, price_from, price_until)
    return GenResponse(**val)