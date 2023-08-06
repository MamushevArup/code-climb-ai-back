from fastapi import Depends, HTTPException, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

@router.post("/shanyraks/{id:str}/decline")
def decline_for_moderators(
    house_id:str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    if jwt_data.role != "moderator":
        raise HTTPException(status_code=403, detail="You are not moderator sorry!!!")
    svc.repository.delete_for_moderators(house_id)
    return Response(status_code=200)