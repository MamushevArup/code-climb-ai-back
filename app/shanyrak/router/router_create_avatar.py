from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from fastapi import Response, Depends, UploadFile
from . import router

@router.post("/auth/users/me")
def updload_avatar_id( 
    file : UploadFile,
    jwt_data : JWTData = Depends(parse_jwt_user_data),
    svc : Service = Depends(get_service)
):
    val = svc.s3_service.upload_file(file.file, file.filename)
    svc.repository.upload_avatar(jwt_data.user_id, val)
    return Response(status_code=200)