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


@user_control_api.get("/userprojects")
async def get_user_projects_data(Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * project_id  : str

    Returns
    -------
    Project Infomation

    """

    _, token_data = Authentication.verify_token(Authorization)

    response = UserMangement.get_user_projects(token_data)

    return response


@user_control_api.get("/userdatasets")
async def get_user_datasets(Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * project_id  : str

    Returns
    -------
    Project Infomation

    """

    _, token_data = Authentication.verify_token(Authorization)

    response = UserMangement.get_user_datasets(token_data)

    return response


@user_control_api.get("/dataset/{dataset_uuid}")
async def get_user_dataset(dataset_uuid, Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * project_id  : str

    Returns
    -------
    Project Infomation

    """

    Authentication.verify_token(Authorization)

    response = UserMangement.get_user_dataset(dataset_uuid)

    return response


@user_control_api.get("/get-followers")
async def get_follower(Authorization:Optional[str]=Header(None)):
    
    _,token =  Authentication.verify_token(Authorization)

    respones = UserMangement.get_followers(token)
    
    return respones

@user_control_api.get("/get-following")
async def get_follower(Authorization:Optional[str]=Header(None)):
    
    _,token =  Authentication.verify_token(Authorization)

    respones = UserMangement.get_following(token)
    
    return respones