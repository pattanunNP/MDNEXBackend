import uuid
from typing import Optional
from service.UserMangement import UserMangement
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header


user_control_api = APIRouter()


# acess controller
@user_control_api.get("/search")
async def search_user(query: str, Authorization: Optional[str] = Header(None)):

    """
    เป็น API สำหรับการ Search User
    Parameters
    ----------
    data : pydantic
    * username  : str
  
    
    Returns
    -------
    username, email, uuid

    """

    _, data = Authentication.verify_token(Authorization)

    response = UserMangement.search_user(query, data)

    return response


@user_control_api.get("/dashboard")
async def getUserData(Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * project_name  : str
    * project_description : Optional[str] = None
    Returns
    -------
    Token 

    """

    _, data = Authentication.verify_token(Authorization)

    response = UserMangement.get_userData(data)

    return response
