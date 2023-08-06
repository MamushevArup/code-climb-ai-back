from datetime import datetime
from typing import List
from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from ...auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.utils import AppModel
from . import router

class SaveRequest(AppModel):
    user_id:str
    created_at:datetime
    question:List
    user_answer:str | None
    right_answer:str | None

@router.get("/api/chat")
def generate_response(
    svc:Service=Depends(get_service),
    jwt_data:JWTData=Depends(parse_jwt_user_data)
):
    language = svc.repository.get_language_db(jwt_data.user_id)
    get_question_gpt = svc.openai.create_list_question(language)
    # and remove any leading or trailing spaces
    cleaned_questions = [question.strip().lstrip("0123456789. ") for question in get_question_gpt if question.strip().endswith("?")]

    list_db = svc.repository.add_list_question(jwt_data.user_id, cleaned_questions)
    
    if list_db is not None:
        return cleaned_questions
    # internet = svc.openai.search_internet(get_question_gpt)
    # svc.repository.update_gpt_right_answer(save_question, internet)