from fastapi import Depends, Response
from app.utils import AppModel
from app.shanyrak.service import Service, get_service
from . import router

class RequestUpdate(AppModel):
    email:str
    lang:str

@router.patch("/createUser")
def patch(
    payload:RequestUpdate,
    svc:Service=Depends(get_service)
):
    val = svc.repository.update_user_lang_db(payload.email, payload.lang)
    print(val)
    return Response(status_code=200)