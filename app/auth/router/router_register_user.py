from fastapi import Depends, Response
from app.utils import AppModel
from fastapi.security import OAuth2PasswordRequestForm
from ..service import Service, get_service
from . import router


class AuthorizeUserResponse(AppModel):
    access_token: str
    token_type: str = "Bearer"

@router.post(
    "/users", response_model=AuthorizeUserResponse
)
def register_user(
    response: Response,
    input: OAuth2PasswordRequestForm = Depends(),
    svc: Service = Depends(get_service),# Include the Response object
) -> AuthorizeUserResponse:
    user_exists = svc.repository.get_user_by_email(input.username)
    print(input)
    if user_exists:
        svc.repository.update_user_by_email(input.username)
        access_token = svc.jwt_svc.create_access_token(user=user_exists)
    else:
        svc.repository.create_user(input.username, input.password, ''.join(input.scopes))
        get_user = svc.repository.get_user_by_email(input.username)
        access_token = svc.jwt_svc.create_access_token(user=get_user)
    print(''.join(input.scopes))
    # Set the access_token as an HttpOnly cookie
    
    data = AuthorizeUserResponse(access_token=access_token)
    response.set_cookie(
        key="access_token",
        value=data.access_token,
        httponly=True,
        max_age=3600,  # Set the expiration time as per your requirements
        secure=True,  # Set to True for HTTPS connections
        samesite="strict"  # Set the desired SameSite attribute value
    )
    print(data.access_token)
    return data