from fastapi import Depends, Response, UploadFile
from app.utils import AppModel
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router


@router.patch("/image")
def choose_lang(
    input:UploadFile,
    svc:Service=Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):  
    print(input)
    url = svc.s3_service.upload_file(input.file, input.filename)
    get_prev_image = svc.repository.get_language_db(jwt_data.user_id)
    svc.repository.upload_image_s3(jwt_data.user_id, url)
    delete = svc.s3_service.delete_file(get_prev_image["image_url"])
    print(delete)
    return {"url" : url}
    