import uuid
from typing import Optional

from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header


fileupload_control_api = APIRouter()


# acess controller
@fileupload_control_api.post("/files/upload")
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

    return response

