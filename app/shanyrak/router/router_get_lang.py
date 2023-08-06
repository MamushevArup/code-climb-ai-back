from fastapi import Depends
from app.utils import AppModel
from ...shanyrak.service import Service, get_service
from . import router

class Response(AppModel):
    lang:str

class LangRequest(AppModel):
    email : str

@router.get("/getLang", response_model=Response)
def get_l(
    data:LangRequest,
    svc:Service=Depends(get_service)
):
    val = svc.repository.get_lang(data.email)
    return Response(**val)