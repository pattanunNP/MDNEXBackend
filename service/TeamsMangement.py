from starlette import responses
import config as ENV
from fastapi import HTTPException
from utils.Recorddata import Recorddata
import uuid
import pendulum, random
from datetime import datetime

class TeamsMangement:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore
    teamprojectStore = Recorddata.teamprojectstore

    @staticmethod
    def create_team(team_name, token_data, team_description=None):

        team_uuid = str(uuid.uuid4())
        team_object = {
            "team_name": team_name,
            "team_uuid": team_uuid,
            "team_description": team_description,
            "team_admin_uuid": token_data["uuid"],
            "team_last_modified":datetime.now(),
            "team_created_time":datetime.now(),
            "team_modified_log": {
                0: {
                   
                    "uuid": token_data["uuid"],
                    "action": "create_team",
                    "timestamp":datetime.now(),
                }
            },
            "team_project": [],
            "team_members": {
                0: {
                   
                    "uuid": token_data["uuid"],
                    "role": "team_admin",
                    "timestamp":datetime.now(),
                }
            },
            "message": "team was created",
        }

        TeamsMangement.teamStore.insert_one(
            {
                "team_name": team_name,
                "team_uuid": team_uuid,
                "team_description": team_description,
                "team_admin_uuid": token_data["uuid"],
                "team_last_modified": datetime.now(),
                "team_created_time": datetime.now(),
                "team_modified_log": [
                    {
                       
                        "uuid": token_data["uuid"],
                        "action": "create_team",
                        "timestamp":datetime.now()
                    }
                ],
                "team_members": [
                    {
                        
                        "uuid": token_data["uuid"],
                        "role": "team_admin",
                        "timestamp":datetime.now()
                    }
                ],
                "team_projects": [],
            }
        )
        TeamsMangement.userDocuments.find_one_and_update(
            {"uuid": token_data["uuid"]}, {"$push": {"teams": team_uuid}}
        )
        try:
            TeamsMangement.userDocuments.create_index([("team_uuid", "text")])
            TeamsMangement.userDocuments.create_index([("team_admin_uuid", "text")])
            TeamsMangement.userDocuments.create_index([("team_admin_name", "text")])

        except:
            pass

        return team_object

    @staticmethod
    def get_teams(team_admin_uuid):
        teams = {}
        team_obj = {}

        for i, team in enumerate(
            TeamsMangement.teamStore.find({"team_admin_uuid": team_admin_uuid})
        ):
            team_obj = {
                "_id": str(team["_id"]),
                "team_uuid": team["team_uuid"],
                "team_admin_uuid": team["team_admin_uuid"],
                "team_last_modified": team["team_last_modified"],
                "team_created_time": team["team_created_time"],
                "team_modified_log": team["team_modified_log"],
                "team_projects": team["team_projects"],
                "team_members": team["team_member"],
            }

            teams[i] = team_obj

        response = {"teams": teams, "lasted_query": pendulum.now(tz="Asia/Bangkok")}

        return response

    @staticmethod
    def check_teamAdmin(team_uuid):
        try:
            team_data = TeamsMangement.teamStore.find_one({"team_uuid": team_uuid})
            team_admin = team_data["team_admin_uuid"]

        except:
            team_admin = None

        return team_admin

    @staticmethod
    def add_member(team_uuid, token_data, team_member):

        uuid_key = token_data["uuid"]
        team_admin = TeamsMangement.check_teamAdmin(team_uuid)

        if team_admin is not None:

            if uuid_key == team_admin:

                {"uuid": token_data["uuid"]},
                {"$push": {"team_members": team_member}}

                response = {"message": ""}
                return response

            else:

                reponse = {
                    "message": "Only team administrator can be add member to team"
                }
                return reponse
        else:
            reponse = {"message": f"Couldn't found Team ID: {team_uuid}"}
            return reponse

    @staticmethod
    def create_teamproject(
        team_uuid, project_name, token_data, project_description=None
    ):

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
            "team_uuid": team_uuid,
            "project_thumbnail": thumbnail_img,
            "project_description": project_description,
            "project_owner_name": token_data["issuer"],
            "project_owner_uuid": token_data["uuid"],
            "project_last_modified": pendulum.now(tz="Asia/Bangkok"),
            "project_created_time": pendulum.now(tz="Asia/Bangkok"),
            "project_modified_log": {
                0: {
                    
                    "uuid": token_data["uuid"],
                    "action": "create_project",
                    "timestamp": pendulum.now(tz="Asia/Bangkok"),
                }
            },
            "project_member": {
                0: {
                   
                    "uuid": token_data["uuid"],
                    "role": "project_owner",
                    "timestamp": pendulum.now(tz="Asia/Bangkok"),
                }
            },
            "project_datasets": {},
            "project_labeltool": {},
            "isTeamProject": True,
            "message": "Project was created",
        }

        TeamsMangement.teamprojectStore.insert_one(
            {
                "project_name": project_name,
                "project_uuid": project_uuid,
                "team_uuid": team_uuid,
                "project_thumbnail": thumbnail_img,
                "project_description": project_description,
                "project_owner_name": token_data["issuer"],
                "project_owner_uuid": token_data["uuid"],
                "project_last_modified": pendulum.now(tz="Asia/Bangkok"),
                "project_created_time": pendulum.now(tz="Asia/Bangkok"),
                "project_modified_log": [
                    {
                       
                        "uuid": token_data["uuid"],
                        "action": "create_project",
                        "timestamp": pendulum.now(tz="Asia/Bangkok"),
                    }
                ],
                "project_members": [
                    {
                       
                        "uuid": token_data["uuid"],
                        "role": "project_owner",
                        "timestamp": pendulum.now(tz="Asia/Bangkok"),
                    }
                ],
                "project_datasets": [],
                "project_labeltool": [],
                "isDeactive": False,
                "isTeamProject": True,
            }
        )

        TeamsMangement.userDocuments.find_one_and_update(
            {"uuid": token_data["uuid"]}, {"$push": {"projects": project_uuid}}
        )

        TeamsMangement.teamStore.find_one_and_update(
            {"team_uuid": team_uuid}, {"$push": {"team_projects": project_uuid}}
        )

        return project_object

    @staticmethod
    def delete_team(team_uuid, token_data):

        uuid_key = token_data["uuid"]
        team_admin = TeamsMangement.check_teamAdmin(team_uuid)

        if team_admin is not None:
            if uuid_key == team_admin:
                response = {"message": f"Team ID: {team_uuid} was deleted"}

                TeamsMangement.teamStore.delete_one({"team_uuid": team_uuid})

                return response

            else:

                reponse = {"message": "Only team administrator can be delete the team"}
                return reponse
        else:
            reponse = {"message": f"Couldn't found Team ID: {team_uuid}"}
            return reponse

