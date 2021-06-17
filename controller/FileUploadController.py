from typing import Optional, List
from service.FileUploadMangement import FileUploadMangement
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header, File, UploadFile
from .Schema import (
    CreateDataset,
    UpdateDataset,
    AddDatasetToProject,
    RemoveDatasetToProject,
)

fileupload_control_api = APIRouter()


# acess controller
@fileupload_control_api.post("/dataset/upload")
async def upload_dataset(
    dataset_name: str,
    dataset_uuid: str,
    files: List[UploadFile] = File(...),
    Authorization: Optional[str] = Header(None),
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

    response = FileUploadMangement.UploadFile(
        file_content_list, dataset_name, dataset_uuid, filename_list, data
    )

    return response


@fileupload_control_api.post("/dataset/newdata")
async def create_dataset(
    data: CreateDataset, Authorization: Optional[str] = Header(None)
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
    dataset_name = data.dataset_name

    dataset_description = data.dataset_description

    _, token_data = Authentication.verify_token(Authorization)

    response = FileUploadMangement.CreateDataset(
        dataset_name, token_data, dataset_description,
    )

    return response


@fileupload_control_api.post("/dataset/add-to-project")
async def add_dataset_to_project(
    data: AddDatasetToProject, Authorization: Optional[str] = Header(None)
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
    project_uuid = data.project_uuid
    dataset_uuid = data.dataset_uuid

    _, token_data = Authentication.verify_token(Authorization)

    response = FileUploadMangement.AddDatasetToProject(
        project_uuid, dataset_uuid, token_data
    )

    return response


@fileupload_control_api.post("/dataset/remove-from-project")
async def remove_dataset_to_project(
    data: RemoveDatasetToProject, Authorization: Optional[str] = Header(None)
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
    project_uuid = data.project_uuid
    dataset_uuid = data.dataset_uuid

    _, token_data = Authentication.verify_token(Authorization)

    response = FileUploadMangement.RemoveDatasetToProject(
        project_uuid, dataset_uuid, token_data
    )

    return response


@fileupload_control_api.post("/dataset/update")
async def search_user(
    payload: UpdateDataset,
    dataset_name: str,
    dataset_uuid: str,
    Authorization: Optional[str] = Header(None),
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

    _, token_data = Authentication.verify_token(Authorization)

    response = FileUploadMangement.UpdateDataset(
        action_type=payload.action_type,
        content=payload.datasetfiles,
        dataset_name=dataset_name,
        dataset_uuid=dataset_uuid,
        token_data=token_data,
    )

    return response

