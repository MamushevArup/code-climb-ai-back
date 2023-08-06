from fastapi import Depends
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router

@router.get("/getData")
def get_data_from_db(
    svc:Service=Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
): 
    user = svc.repository.get_language_db(jwt_data.user_id)
    count_language = svc.repository.get_technology_count(jwt_data.user_id)
    print(user)
    hmap = {}
    for i in count_language:
        hmap[i["language"]] = i["count"]
    obj =  {"user": user, "count_language": hmap}
    print(obj)
    return obj