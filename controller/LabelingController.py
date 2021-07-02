from typing import Optional, List

from fastapi import responses
from service.Labeling import LabelingTool
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header, File, UploadFile
from fastapi.responses import FileResponse

labeling_control_api = APIRouter()


# acess controller
@labeling_control_api.post("/labeling/auto-edgedetection")
async def search_user(
    theshold1: Optional[int],
    theshold2: Optional[int],
    algorithm: Optional[str],
    Image: UploadFile = File(...),
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
    filename = Image.filename

    file_content = await Image.read()

    Authentication.verify_token(Authorization)

    result = LabelingTool.autoEdgeDetection(
        file_content, filename, algorithm, theshold1, theshold2
    )

    return result


@labeling_control_api.post("/labeling/create-task")
async def createTask(
    project_id: str,
    spec_user: Optional[str],
    Authorization: Optional[str] = Header(None),
):
    _, token = Authentication.verify_token(Authorization)

    responses = LabelingTool.create_task(project_id, token, spec_user)

    return responses


@labeling_control_api.get("/labeling/getimage")
async def getImage(
    project_id: str,
    dataset_id: str,
    file_id: str,
    Authorization: Optional[str] = Header(None),
):
    _, token = Authentication.verify_token(Authorization)
    responses = LabelingTool.getimage(project_id, dataset_id, file_id, token)
    return responses


@labeling_control_api.get("/labeling")
async def label(
    project_id: str,
    dataset_id: str,
    file_id: str,
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
    _, token = Authentication.verify_token(Authorization)

    LabelingTool.edit(project_id, dataset_id, file_id, token)
    return "result"

