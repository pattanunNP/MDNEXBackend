import pprint
import re
from pendulum import date
from starlette import responses
import config as ENV
from fastapi import HTTPException
from utils.Recorddata import Recorddata
import uuid
import pendulum
from datetime import datetime


class UserMangement:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore
    dataStore = Recorddata.datastore

    @staticmethod
    def search_user(query, token_data):
        response = {}
        users_match = []

        if len(query) > 0:

            for i, user in enumerate(
                UserMangement.userDocuments.find(
                    {"username": {"$regex": f"{query}", "$options": "i"}}
                ).limit(100)
            ):
                if user["uuid"] != token_data["uuid"]:
                    user_obj = {
                        "_id": str(user["_id"]),
                        "regex": query,
                        "email": user["email"],
                        "uuid": user["uuid"],
                        "role": user["role"],
                        "profileimage": user["profile_photo"],
                        "username": user["username"],
                    }
                    users_match.append(user_obj)

            response = {
                "match": users_match,
                "lasted_query": pendulum.now(tz="Asia/Bangkok"),
            }

        else:
            response = {
                "queryString": f"{query}",
                "match": [],
                "lasted_query": pendulum.now(tz="Asia/Bangkok"),
            }
        return response

    @staticmethod
    def get_userData(token_data):
        response = {}

        result = UserMangement.userDocuments.find_one({"uuid": token_data["uuid"]})

        count_projects = len(result["projects"])
        count_teams = len(result["teams"])

        response = {
            "profileImage": result["profile_photo"],
            "email": result["email"],
            "projects": result["projects"],
            "count_teams": count_teams,
            "count_images": 0,
            "count_projects": count_projects,
            "uuid": result["uuid"],
            "username": result["username"],
            "role": result["role"],
            "teams": result["teams"],
            "datasets":result["datasets"],
            "Bio":result["Bio"],
            "Followers":result["Followers"],
            "Following":result["Following"],
            "message": "Success",
        }

        return response

    @staticmethod
    def get_user_projects(token_data):
        projects_data = {}
        projects_match = []

        for i, result in enumerate(
            UserMangement.projectStore.find(
                {"project_members": {"$elemMatch": {"uuid": token_data["uuid"]}}}
            )
        ):

            project_data_obj = {
                "_id": str(result["_id"]),
                "project_name": result["project_name"],
                "project_uuid": result["project_uuid"],
                "project_thumbnail": result["project_thumbnail"],
                "project_description": result["project_description"],
               
                "project_owner_uuid": result["project_owner_uuid"],
                "project_last_modified": result["project_last_modified"],
                "project_created_time": result["project_created_time"],
                "project_modified_log": result["project_modified_log"],
                "project_members": result["project_members"],
                "project_datasets": result["project_datasets"],
                "project_labeltool": result["project_labeltool"],
                "isDeactive": result["isDeactive"],
            }

            projects_match.append(project_data_obj)

        projects_data = {
            "match": projects_match,
        }
        return projects_data

    @staticmethod
    def get_user_datasets(token_data):
        datasets_data = {}
        dataset_match = []

        for i, result in enumerate(
            UserMangement.dataStore.find({"dataset_owner_uuid": token_data["uuid"]})
        ):
            number_of_images = len(result["dataset_files"])
            data_obj = {
                "_id": str(result["_id"]),
                "dataset_name": result["dataset_name"],
                "dataset_uuid": result["dataset_uuid"],
                "dataset_description": result["dataset_description"],
                "dataset_thumbnail": result["dataset_thumbnail"],
                "dataset_owner_uuid": result["dataset_owner_uuid"],
                "dataset_last_modified": result["dataset_last_modified"],
                "dataset_created_time": result["dataset_created_time"],
                "dataset_modified_log": result["dataset_modified_log"],
                "dataset_members": result["dataset_members"],
                "isDeactive": result["isDeactive"],
                "dataset_files": result["dataset_files"],
                "dataset_atteched_project": result["dataset_atteched_project"],
                "dataset_number_of_images": number_of_images,
            }

            dataset_match.append(data_obj)

        datasets_data = {
            "match": dataset_match,
        }
        return datasets_data

    @staticmethod
    def get_user_dataset(dataset_uuid):
        datasets_data = {}

        result = UserMangement.dataStore.find_one({"dataset_uuid": dataset_uuid})
        number_of_images = len(result["dataset_files"])
        # print(result)
        datasets_data = {
            "dataset_name": result["dataset_name"],
            "dataset_uuid": result["dataset_uuid"],
            "dataset_description": result["dataset_description"],
            "dataset_thumbnail": result["dataset_thumbnail"],
            "dataset_owner_uuid": result["dataset_owner_uuid"],
            "dataset_last_modified": result["dataset_last_modified"],
            "dataset_created_time": result["dataset_created_time"],
            "dataset_modified_log": result["dataset_modified_log"],
            "dataset_members": result["dataset_members"],
            "isDeactive": result["isDeactive"],
            "dataset_files": result["dataset_files"],
            "dataset_number_of_images": number_of_images,
        }

        return datasets_data


    @staticmethod
    def get_followers(token):
        followers_list=[]
        responses = {}
        
        results = UserMangement.userDocuments.aggregate([
            {
                '$match': {
                    'uuid': token['uuid']
                }
            }, {
                '$unwind': {
                    'path': '$Followers'
                }
            }, {
                '$lookup': {
                    'from': 'userdocuments', 
                    'localField': 'Followers.uuid', 
                    'foreignField': 'uuid', 
                    'as': 'Followers.Followers_info'
                }
            }, {
                '$unwind': {
                    'path': '$Followers.Followers_info'
                }
            }, {
                '$group': {
                    '_id': '$_id', 
                    'username': {
                        '$first': '$username'
                    }, 
                    'uuid': {
                        '$first': '$uuid'
                    }, 
                    'role': {
                        '$first': '$role'
                    }, 
                    'profile_photo': {
                        '$first': '$profile_photo'
                    }, 
                    'Followers': {
                        '$push': '$Followers'
                    }
                }
            }
        ])

        for result in  results :
           
            _id = str(result['_id'])
            info={}
            # print(result)
            
            for follower in result["Followers"]:

                member_info = follower["Followers_info"]
                info={
                    "_id":str(member_info["_id"]),
                    "email":member_info["email"],
                    "username":member_info["username"],
                    "profile_photo":member_info["profile_photo"],
                    "uuid":member_info["uuid"],
                
                    
                }
                followers_list.append(info)
    
        responses = {

               
               "message":"followers",
                "info":followers_list
                
            }
            

        return responses



    
    @staticmethod
    def get_following(token):
        following_list=[]
        responses = {}
        
        
        results = UserMangement.userDocuments.aggregate([
            {
                '$match': {
                    'uuid': token['uuid']
                }
            }, {
                '$unwind': {
                    'path': '$Following'
                }
            }, {
                '$lookup': {
                    'from': 'userdocuments', 
                    'localField': 'Following.uuid', 
                    'foreignField': 'uuid', 
                    'as': 'Following.Following_info'
                }
            }, {
                '$unwind': {
                    'path': '$Following.Following_info'
                }
            }, {
                '$group': {
                    '_id': '$_id', 
                    'username': {
                        '$first': '$username'
                    }, 
                    'uuid': {
                        '$first': '$uuid'
                    }, 
                    'role': {
                        '$first': '$role'
                    }, 
                    'profile_photo': {
                        '$first': '$profile_photo'
                    }, 
                    'Following': {
                        '$push': '$Following'
                    }
                }
            }
        ])
        # print(results)
        for result in  results:
            _id = str(result['_id'])
            
            info={}
            # print(result)
            
            for follower in result["Following"]:

                member_info = follower["Following_info"]
                info={
                    "_id":str(member_info["_id"]),
                    "email":member_info["email"],
                    "username":member_info["username"],
                    "profile_photo":member_info["profile_photo"],
                    "uuid":member_info["uuid"],
                
                    
                }
                following_list.append(info)
       
        responses = {
                "message":"following",
                "info":following_list
                
            }
            

        return responses