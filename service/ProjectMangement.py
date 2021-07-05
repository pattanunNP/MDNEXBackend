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
            "project_owner_uuid": token_data["uuid"],
            "project_last_modified": pendulum.now(),
            "project_created_time": pendulum.now(),
            "project_modified_log": {
                0: {
                  
                    "uuid": token_data["uuid"],
                    "action": "create_project",
                    "timestamp":datetime.now(),
                }
            },
            "project_member": {
                0: {
                    
                    "uuid": token_data["uuid"],
                    "role": "project_owner",
                    "timestamp":datetime.now(),
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
                "project_owner_uuid": token_data["uuid"],
                "project_last_modified": datetime.now(),
                "project_created_time": datetime.now(),
                "project_modified_log": [
                    {
                        "uuid": token_data["uuid"],
                        "action": "create_project",
                        "timestamp":datetime.now()
                        
                    }
                ],
                "project_members": [
                    {
                       
                        "uuid": token_data["uuid"],
                      "timestamp":datetime.now()
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
  
        project_members =[]

        results = ProjectMangement.projectStore.aggregate([
        {
            '$match': {
                'project_uuid': project_id
            }
        }, {
            '$unwind': {
                'path': '$project_members'
            }
        }, {
            '$lookup': {
                'from': 'userdocuments', 
                'localField': 'project_members.uuid', 
                'foreignField': 'uuid', 
                'as': 'project_members.member_info'
            }
        }, {
            '$unwind': {
                'path': '$project_members.member_info'
            }
        }, {
            '$group': {
                '_id': '$_id', 
                'project_name': {
                    '$first': '$project_name'
                }, 
                'project_uuid': {
                    '$first': '$project_uuid'
                }, 
                'project_thumbnail': {
                    '$first': '$project_thumbnail'
                }, 
                'project_description': {
                    '$first': '$project_description'
                }, 
                'project_owner_uuid': {
                    '$first': '$project_owner_uuid'
                }, 
                'project_modified_log': {
                    '$first': '$project_modified_log'
                }, 
                'project_last_modified': {
                    '$first': '$project_last_modified'
                }, 
                'project_created_time': {
                    '$first': '$project_created_time'
                }, 
                'project_labeltool': {
                    '$first': '$project_labeltool'
                }, 
                'project_datasets': {
                    '$first': '$project_datasets'
                }, 
                'isTeamProject': {
                    '$first': '$isTeamProject'
                }, 
                'project_members': {
                    '$push': '$project_members'
                }, 
                'isDeactive': {
                    '$first': '$isDeactive'
                }
            }
        }
    ])
        
        for result in results:
            _id = str(result['_id'])
            
            info={}
            for member in  result["project_members"]:
                uuid = member["uuid"]
                member_info = member["member_info"]
                info={
                    "_id":str(member_info["_id"]),
                    "email":member_info["email"],
                    "username":member_info["username"],
                    "profile_photo":member_info["profile_photo"],
                    "uuid":member_info["uuid"],
                    "role":"admin",
                    "projects":member_info["projects"],
                    "teams":member_info["teams"],
                    

                }

                project_members.append( {"uuid":  uuid,"member_info": info})
              


            project_data = {
                        "_id":_id,
                        "project_name": result["project_name"],
                        "project_uuid": result["project_uuid"],
                        "project_thumbnail": result["project_thumbnail"],
                        "project_description": result["project_description"],
                        "project_owner_uuid": result["project_owner_uuid"],
                        "project_last_modified": result["project_last_modified"],
                        "project_created_time": result["project_created_time"],
                        "project_modified_log": result["project_modified_log"],
                        "project_datasets": result["project_datasets"],
                        "project_labeltool": result["project_labeltool"],
                        "project_members":project_members
                        
                    
                    
                    }

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

