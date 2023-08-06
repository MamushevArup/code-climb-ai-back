from fastapi import Depends, Response
from app.utils import AppModel
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router

class SaveMessage(AppModel):
    question:str

class Hmap(AppModel):
    user_id:str
    saved_message:str

@router.post("/saveMessage")
def save_user_message(
    message:SaveMessage,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    hmap = Hmap(user_id=jwt_data.user_id, saved_message=message.question)
    inserted_value = svc.repository.save_user_message_db(hmap)
    return Response(status_code=200)