from fastapi import Depends, Response
from app.utils import AppModel
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router
class RequestUpdate(AppModel):
    grade: str
    direct: str
    selectedLanguage: str
    selectedFrameworks: list[str]
    selectedTechnologies: list[str]

@router.patch("/chooseLang")
def choose_lang(
    input:RequestUpdate,
    svc:Service=Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):  
    svc.repository.update_user_lang_db(jwt_data.user_id, input.grade, input.direct, input.selectedLanguage, input.selectedFrameworks, input.selectedTechnologies)
    val = svc.repository.technology_count(jwt_data.user_id, input.selectedLanguage)
    if val is None:
        print(val)
        print("User do not choose a language")
    return Response(status_code=200)