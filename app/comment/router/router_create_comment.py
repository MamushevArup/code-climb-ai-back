from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel
from ..service import Service, get_service
from . import router


class CreateCommentRequest(AppModel):
    content:str


@router.post("/shanyraks/{id:str}/comments")
def create_comments(
    house_id : str,
    content: CreateCommentRequest,
    svc : Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    svc.repository.create_comment_shanyrak(content.dict(), house_id)
    return Response(status_code=200)