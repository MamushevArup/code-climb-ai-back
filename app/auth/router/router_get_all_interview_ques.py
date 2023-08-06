from fastapi import Depends
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router

@router.get("/getInterview")
def get_questions_from_db(
    svc:Service=Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
): 
    val = svc.repository.get_all_questions_from_interview(jwt_data.user_id)
    return {"all" : val}

