from fastapi import Depends, Response
from ..service import Service, get_service
from app.utils import AppModel
from . import router

class UpdateRequest(AppModel):
    content : str

@router.patch("/shanyraks/{id}/comments/{comment_id}")
def update_comment(
    id : str,
    comment_id:str,
    text : UpdateRequest,
    svc : Service = Depends(get_service)
):
    svc.repository.update_comment_by_id(id, comment_id, text.dict())
    return Response(status_code=200)