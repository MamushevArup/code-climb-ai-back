from typing import Any
from fastapi import Cookie, Depends, Response
from fastapi.responses import JSONResponse
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router

class RequestQuestionAndAnswer(AppModel):
    question:str
    answer:str

class SaveQuestion(AppModel):
    user_id:str
    list_question_id:Any
    question:str
    user_answer:str
    right_answer:str | None

@router.post("/get/question/{id}")
def return_one_question(
    id:int,
    input:RequestQuestionAndAnswer,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict :

    get_list, list_id = svc.repository.get_list_question(jwt_data.user_id)
    print(get_list)
    result = []
    for i in get_list:
        result.append(i)
    get_feedback = "\nLet's go"
    if id >0:
        input.question = result[id-1]
        get_feedback = svc.openai.get_feedback_one_question(jwt_data.user_id, input.question, input.answer)
        
        question_data = SaveQuestion(user_id=jwt_data.user_id,list_question_id=list_id, question=input.question, user_answer=input.answer)
        insert_database = svc.repository.save_gpt_question(question_data.dict())

    if id == len(get_list):
        id = 0
        obj = {"status" : 200, "message" : "You are finished thank you"}
        return JSONResponse(
            status_code=206,
            content={ "message" : get_feedback +  "\n\nYou are finished thank you"}
        )
    val = result[id]
    # internet = svc.openai.search_internet(get_question_gpt)
    # svc.repository.update_gpt_right_answer(save_question, internet)
    obj = {
        "message" : get_feedback + "\n\n" + str(id+1) + ". " +val,
        "question" : val
    }
    return obj