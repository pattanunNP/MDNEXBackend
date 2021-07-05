from typing import Optional, List
from .Schema import CreateTask
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


@labeling_control_api.post("/labeling/create/task")
async def createTask(
    project_id: str,
    task:CreateTask,
    Authorization: Optional[str] = Header(None),
):
    _, token = Authentication.verify_token(Authorization)

    task_name = task.task_name
    task_desciption = task.task_description
    task_due_date = task.due_date
    task_labelers = task.labelers
    task_mode = task.mode

    responses = LabelingTool.create_task(project_id,task_name,task_labelers, token, task_mode,task_due_date ,task_desciption)

    return responses


@labeling_control_api.get("/labeling/getimage")
async def getImage(
    task_id: str,
    queue_id:str,
    Authorization: Optional[str] = Header(None),
):
    _, token = Authentication.verify_token(Authorization)
    responses = LabelingTool.getimage(task_id,queue_id, token)
    return responses



@labeling_control_api.get("/labeling/gettasks")
async def getTask(
    task_id: str,
    Authorization: Optional[str] = Header(None),
):
    _, token = Authentication.verify_token(Authorization)
    responses = LabelingTool.get_tasks(task_id, token)
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

