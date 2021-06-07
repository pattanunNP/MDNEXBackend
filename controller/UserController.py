import uuid
from typing import Optional
from service.UserMangement import UserMangemnet
from .Schema import Register, Login, SendVerifyEmail
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter,Header

  
user_control_api = APIRouter()


# acess controller 
@user_control_api.get('/search/user')
async def search_user(query:str, Authorization: Optional[str] = Header(None)):

    """
    เป็น API สำหรับการสร้าง User
    Parameters
    ----------
    data : pydantic
    * username  : str
    * password : str
    * email  : str
    
    Returns
    -------
    user, hashpassword, email, uuid

    """
    

    _, data = Authentication.verify_token(Authorization)

    response = UserMangemnet.search_user(query, data)
 

    return response 


