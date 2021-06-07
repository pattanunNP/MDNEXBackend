import requests
from .Schema import Register, Login,SendVerifyEmail
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Response
from starlette.responses import RedirectResponse
import config as ENV

acess_control_api = APIRouter()


# acess controller 
@acess_control_api.post('/register')
async def register(data: Register):

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
    username = data.username
    password = data.password
    email = data.email

    response = Authentication.register(username, email, password)
 

    return response 

@acess_control_api.post('/send/confrim-email')
async def send_confrim_email(data: SendVerifyEmail):

    username = data.username
    email = data.email
    profile_uuid = data.profile_uuid

    response = Authentication.send_verify_email(username, email, profile_uuid)

    return response

@acess_control_api.get('/confrim/email')
async def confrim_email(verify_token:str):

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
    state isVerified

    """
 

    response = Authentication.confrim_email(verify_token)

    url = f"{ENV.FRONTEND_URL}/verify/email?uuid={response['uuid']}"
    response = RedirectResponse(url=url)

    return response


@acess_control_api.get('/check/verify-email')
async def confrim_email(uuid:str):

    """
    เป็น API สำหรับการสร้าง User
    Parameters
    ----------
    data : pydantic
    * uuid : str
    
    
    Returns
    -------
    state isVerified

    """
 

    response = Authentication.check_verify_email(uuid)
    
    return response

@acess_control_api.post('/login')
async def login(data: Login):
    """
    เป็น API สำหรับการสร้าง User
    Parameters
    ----------
    data : pydantic
    * username  : str
    * password : str
    Returns
    -------
    Token 

    """

    username = data.username
    password = data.password

    response = Authentication.login(username, password)

    return response
