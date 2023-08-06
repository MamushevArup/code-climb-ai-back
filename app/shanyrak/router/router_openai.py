from fastapi import Depends, Response
from ..service import Service, get_service
from app.utils import AppModel
from . import router

class Text(AppModel):
    text:str

@router.post("/openai")
def generate_response(
    val : str,
    svc:Service=Depends(get_service)
):
    ss = svc.openai.finish_prompt(val)
    return ss["choices"]