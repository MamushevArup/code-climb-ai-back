from fastapi import Depends, Response
from app.utils import AppModel
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router

@router.get("/hash")
def hash_return(
    svc:Service=Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):  
    val = svc.repository.get_hash(jwt_data.user_id)

    return val