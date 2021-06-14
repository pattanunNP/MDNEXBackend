from .Schema import CreateProject, DeleteProject, AddProject2Team
from service.ProjectMangement import ProjectMangement

from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header
from typing import Optional

projects_control_api = APIRouter()


@projects_control_api.post("/create/project")
async def create_project(
    data: CreateProject, Authorization: Optional[str] = Header(None)
):
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

    project_name = data.project_name
    project_description = data.project_description

    _, data = Authentication.verify_token(Authorization)

    response = ProjectMangement.create_projects(project_name, data, project_description)

    return response


@projects_control_api.get("/project/{project_id}")
async def get_projec_data(project_id, Authorization: Optional[str] = Header(None)):
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

    response = ProjectMangement.get_project_data(project_id)

    return response


@projects_control_api.get("/userproject")
async def get_projec_data(Authorization: Optional[str] = Header(None)):
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

    response = ProjectMangement.get_project_data(token_data)

    return response


@projects_control_api.post("/add/project-team")
async def add_project_to_team(
    data: AddProject2Team, Authorization: Optional[str] = Header(None)
):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * team_id  : str
    
    Returns
    -------
    Token 

    """

    project_uuid = data.project_uuid
    team_uuid = data.team_uuid

    _, data = Authentication.verify_token(Authorization)

    response = ProjectMangement.add_project_to_team(team_uuid, project_uuid, data)

    return response


@projects_control_api.post("/delete/project")
async def delete_project(
    data: DeleteProject, Authorization: Optional[str] = Header(None)
):
    """
    เป็น API สำหรับการลบ Project
    Parameters
    ----------
    data : pydantic
    * project_uid  : str

    Returns
    -------
    Token 

    """

    project_name = data.project_uuid

    _, data = Authentication.verify_token(Authorization)

    response = ProjectMangement.delete_project(project_name, data)

    return response
