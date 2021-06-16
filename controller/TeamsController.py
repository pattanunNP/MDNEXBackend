from .Schema import CreateTeam, DeleteTeam, AddTeamMembers, CreateTeamProject
from service.TeamsMangement import TeamsMangement
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header
from typing import Optional

teams_control_api = APIRouter()


@teams_control_api.post("/create/team")
async def create_team(data: CreateTeam, Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * team_name  : str
    * team_description : Optional[str] = None
    Returns
    -------
    Token 

    """

    team_name = data.team_name
    team_description = data.team_description

    _, data = Authentication.verify_token(Authorization)

    response = TeamsMangement.create_team(team_name, data, team_description)

    return response


@teams_control_api.post("/create/team-projects")
async def create_team(
    data: CreateTeamProject, Authorization: Optional[str] = Header(None)
):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * team_name  : str
    * team_description : Optional[str] = None
    Returns
    -------
    Token 

    """

    project_name = data.project_name
    project_description = data.project_description
    team_uuid = data.team_uuid

    _, data = Authentication.verify_token(Authorization)

    response = TeamsMangement.create_teamproject(
        team_uuid, project_name, data, project_description
    )

    return response


@teams_control_api.get("/query/team")
async def get_team(user_id: str, Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * team_name  : str
    * team_description : Optional[str] = None
    Returns
    -------
    Token 

    """

    _, data = Authentication.verify_token(Authorization)

    response = TeamsMangement.get_teams(user_id)

    return response


@teams_control_api.post("/add/member")
async def add_member(data: AddTeamMembers, Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการสร้าง Project
    Parameters
    ----------
    data : pydantic
    * team_name  : str
    * team_description : Optional[str] = None
    Returns
    -------
    Token 

    """

    team_member = data.team_mate_email

    _, data = Authentication.verify_token(Authorization)

    response = TeamsMangement.add_member(team_member)

    return response


@teams_control_api.delete("/delete/team")
async def delete_team(data: DeleteTeam, Authorization: Optional[str] = Header(None)):
    """
    เป็น API สำหรับการลบ Project
    Parameters
    ----------
    data : pydantic
    * team_uid  : str

    Returns
    -------
    Token 

    """

    team_uuid = data.team_uuid

    _, data = Authentication.verify_token(Authorization)

    response = TeamsMangement.delete_team(team_uuid, data)

    return response

