from typing import Optional, List
from service.FileUploadMangement import FileUploadMangement
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header, File, UploadFile
from .Schema import CreateDataset

fileupload_control_api = APIRouter()


# acess controller
@fileupload_control_api.post("/dataset/upload")
async def upload_dataset(
    files: List[UploadFile] = File(...), Authorization: Optional[str] = Header(None)
):

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
    filename_list = [file.filename for file in files]

    file_content_list = [await file.read() for file in files]

    _, data = Authentication.verify_token(Authorization)

    response = FileUploadMangement.UploadFile(file_content_list, filename_list, data)

    print(response)

    return response


@fileupload_control_api.post("/dataset/newdata")
async def search_user(data: CreateDataset, Authorization: Optional[str] = Header(None)):

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
    dataset_name = data.dataset_name

    dataset_description = data.dataset_description

    _, token_data = Authentication.verify_token(Authorization)

    response = FileUploadMangement.CreateDataset(
        dataset_description, token_data, dataset_description,
    )

    print(response)

    return response

