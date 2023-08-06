from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from . import router

@router.get("/in")
def updload_file_id(
):
    return {"val" : "Hey"}