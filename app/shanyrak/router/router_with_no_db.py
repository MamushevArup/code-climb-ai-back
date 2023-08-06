from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router

@router.get("/in")
def updload_file_id(

    jwt_data:JWTData=Depends(parse_jwt_user_data),
):
    return {"val" : jwt_data.user_id}