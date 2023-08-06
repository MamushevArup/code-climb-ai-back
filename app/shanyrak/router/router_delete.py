from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.delete("/shanyraks/{id:str}")
def delete_post(
    
    shan_id : str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shan_id = svc.repository.delete_shanyrak(shan_id, jwt_data.user_id, "shanyraq")
    return Response(status_code=200)