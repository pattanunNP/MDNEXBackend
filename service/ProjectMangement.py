import config as ENV
from fastapi import HTTPException
from datetime import datetime
from .TeamsMangement import TeamsMangement
from utils.Recorddata import Recorddata
import uuid
import pendulum
import random


class ProjectMangement:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore
    dataStore = Recorddata.datastore

    @staticmethod
    def create_projects(project_name, token_data, project_description=None):

        bg_list = [
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623682815/MD_NEX/cool-background_mg7zzn.png",
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623682815/MD_NEX/cool-background_2_erfmxs.png",
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623682815/MD_NEX/cool-background_1_jgyzpi.png",
        ]

        thumbnail_img = random.choice(bg_list)
        project_uuid = str(uuid.uuid4())
        project_object = {
            "project_name": project_name,
            "project_uuid": project_uuid,
            "project_thumbnail": thumbnail_img,
            "project_description": project_description,
            "project_owner_name": token_data["issuer"],
            "project_owner_uuid": token_data["uuid"],
            "project_last_modified": pendulum.now(tz="Asia/Bangkok"),
            "project_created_time": pendulum.now(tz="Asia/Bangkok"),
            "project_modified_log": {
                0: {
                    "name": token_data["issuer"],
                    "uuid": token_data["uuid"],
                    "action": "create_project",
                    "timestamp": pendulum.now(tz="Asia/Bangkok"),
                }
            },
            "project_member": {
                0: {
                    "name": token_data["issuer"],
                    "uuid": token_data["uuid"],
                    "role": "project_owner",
                    "timestamp": pendulum.now(tz="Asia/Bangkok"),
                }
            },
            "project_datasets": {},
            "project_labeltool": {},
            "isTeamProject": False,
            "message": "Project was created",
        }

        ProjectMangement.projectStore.insert_one(
            {
                "project_name": project_name,
                "project_uuid": project_uuid,
                "project_thumbnail": thumbnail_img,
                "project_description": project_description,
                "project_owner_name": token_data["issuer"],
                "project_owner_uuid": token_data["uuid"],
                "project_last_modified": pendulum.now(tz="Asia/Bangkok"),
                "project_created_time": pendulum.now(tz="Asia/Bangkok"),
                "project_modified_log": [
                    {
                        "name": token_data["issuer"],
                        "uuid": token_data["uuid"],
                        "action": "create_project",
                        "timestamp": pendulum.now(tz="Asia/Bangkok"),
                    }
                ],
                "project_members": [
                    {
                        "name": token_data["issuer"],
                        "uuid": token_data["uuid"],
                        "role": "project_owner",
                        "timestamp": pendulum.now(tz="Asia/Bangkok"),
                    }
                ],
                "project_datasets": [],
                "project_labeltool": [],
                "isDeactive": False,
                "isTeamProject": False,
            }
        )

        ProjectMangement.userDocuments.find_one_and_update(
            {"uuid": token_data["uuid"]}, {"$push": {"projects": project_uuid}}
        )

        return project_object

    @staticmethod
    def check_owner(project_uuid):
        try:
            project_data = ProjectMangement.projectStore.find_one(
                {"project_uuid": project_uuid}
            )
            project_owner = project_data["project_owner_uuid"]

        except:
            project_owner = None

        return project_owner

    @staticmethod
    def get_project_data(project_id):
        project_data = {}
        try:
            result = ProjectMangement.projectStore.find_one(
                {"project_uuid": project_id}
            )
            project_data = {
                "project_name": result["project_name"],
                "project_uuid": result["project_uuid"],
                "project_thumbnail": result["project_thumbnail"],
                "project_description": result["project_description"],
                "project_owner_name": result["project_owner_name"],
                "project_owner_uuid": result["project_owner_uuid"],
                "project_last_modified": result["project_last_modified"],
                "project_created_time": result["project_created_time"],
                "project_modified_log": result["project_modified_log"],
                "project_members": result["project_members"],
                "project_datasets": result["project_datasets"],
                "project_labeltool": result["project_labeltool"],
            }
        except:
            project_data = None

        return project_data

    @staticmethod
    def add_project_to_team(team_uuid, project_uuid, token_data):

        uuid_key = token_data["uuid"]
        team_admin = TeamsMangement.check_teamAdmin(team_uuid)
        project_owner = ProjectMangement.check_owner(project_uuid)

        print(team_admin, project_owner)

        if team_admin is not None and project_owner is not None:
            if uuid_key == team_admin and uuid_key == project_owner:
                response = {
                    "message": f"Project ID: {project_uuid} was added to {team_uuid}"
                }

                ProjectMangement.teamStore.find_one_and_update(
                    {"team_uuid": team_uuid},
                    {"$addToSet": {"team_projects": project_uuid}},
                )

                return response

            else:

                reponse = {
                    "message": "Only project owner and Team Admin can be delete the project"
                }
                return reponse
        else:
            reponse = {
                "message": f"Couldn't found Team ID: {team_uuid} or Projects ID: {project_uuid}"
            }
            return reponse

    @staticmethod
    def delete_project(project_uuid, token_data):

        uuid_key = token_data["uuid"]
        owner = ProjectMangement.check_owner(project_uuid)

        if owner is not None:
            if uuid_key == owner:
                response = {"message": f"Project ID: {project_uuid} was deleted"}

                ProjectMangement.projectStore.delete_one({"project_uuid": project_uuid})
                ProjectMangement.userDocuments.find_one_and_update(
                    {"uuid": uuid_key}, {"$pull": {"projects": project_uuid}}
                )

                ProjectMangement.dataStore.update_many(
                    {"dataset_atteched_project": project_uuid},
                    {"$pull": {"dataset_atteched_project": project_uuid}},
                )

                return response

            else:

                reponse = {"message": "Only project owner can be delete the project"}
                return reponse
        else:
            reponse = {"message": f"Couldn't found Project ID: {project_uuid}"}
            return reponse

