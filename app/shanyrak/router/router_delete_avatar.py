from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from fastapi import Response, Depends, UploadFile
from . import router

@router.delete("/auth/users/avatar")
def delete_avatar_id( 
    jwt_data : JWTData = Depends(parse_jwt_user_data),
    svc : Service = Depends(get_service)
):
    get = svc.repository.return_ava(jwt_data.user_id)
    res = get["avatar_url"].split("/")[-1]
    val = svc.s3_service.delete_file(res)
    svc.repository.delete_avatar(jwt_data.user_id)
    return Response(status_code=200)