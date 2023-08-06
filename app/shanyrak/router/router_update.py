from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router
from app.utils import AppModel


class UpdatePostRequest(AppModel):
    type : str
    price : int
    address : str
    area : float
    rooms_count : int
    description : str

@router.patch("/shanyraks/{id:str}", )
def update_shanyrak(
    shan_id : str,
    input: UpdatePostRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shan_id = svc.repository.update_shanyrak(shan_id, input.dict(), jwt_data.user_id)
    return Response(status_code=200)