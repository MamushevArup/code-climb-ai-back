from dataclasses import Field
from typing import Any, Optional
from fastapi import Depends
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.utils import AppModel
from . import router

class ReturnField(AppModel):
    _id: Any 
    content: str
    house: Any
    author: Any
class GetCommentIdResponse(AppModel):
    comments: list[ReturnField]

@router.get("/shanyraks/{id:str}/comments", response_model=GetCommentIdResponse)
def get_by_id(
    id: str,
    svs: Service = Depends(get_service),  
    jwt_data: JWTData = Depends(parse_jwt_user_data),
): 
    # This is an array of MongoDB documents
    data = svs.repository.get_comment_by_id(id)
    print(data)
    comments = []
    for doc in data:
        comment = ReturnField(
            _id=doc["_id"],
            content=doc["content"],
            house=doc["house_id"],
            author=jwt_data.user_id
        )
        comments.append(comment)
    return GetCommentIdResponse(comments=comments)
