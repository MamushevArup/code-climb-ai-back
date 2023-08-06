from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.get("/getSaved")
def return_saved_question(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) :
    val = svc.repository.get_saved_db(jwt_data.user_id)
    print(val)
    return val