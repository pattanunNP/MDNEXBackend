from pydantic import BaseModel
from typing import Optional


class Register(BaseModel):
    username: str
    password: str
    email: str
    role: Optional[str] = None


class SendVerifyEmail(BaseModel):
    username: str
    profile_uuid: str
    email: str


class Login(BaseModel):
    username: str
    password: str


class CreateProject(BaseModel):
    project_name: str
    project_description: Optional[str] = None


class AddProject2Team(BaseModel):
    project_uuid: str
    team_uuid: str


class DeleteProject(BaseModel):
    project_uuid: str


class CreateTeam(BaseModel):
    team_name: str
    team_description: Optional[str] = None


class AddTeamMembers(BaseModel):
    team_mate_email: str


class DeleteTeam(BaseModel):
    team_uuid: str


class Refresh(BaseModel):
    refresh_token: str


class CreateDataset(BaseModel):
    dataset_name: str
    dataset_description: Optional[str] = None


class UpdateDataset(BaseModel):
    datasetfiles: Optional[list] = None
    action_type: str

