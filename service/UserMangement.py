import pprint
import re
from starlette import responses
import config as ENV
from fastapi import HTTPException
from utils.Recorddata import  Recorddata
import uuid
import pendulum



class UserMangement:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore


    
    @staticmethod
    def search_user(query, token_data):
        response ={}
        users_match = []

        if len(query)>0:
            
           for i,user in enumerate(UserMangement.userDocuments.find({"username":{"$regex":f"{query}",
                                                                    "$options":"i"}}).limit(100)):
               if user["uuid"] != token_data["uuid"]:                                                          
                    user_obj ={
                        "_id":str(user["_id"]),
                        "regex":query,
                        "email":user["email"],
                        "uuid":user["uuid"],
                        "role":user["role"],
                        "profileimage":user['profile_photo'],
                        "username":user["username"]}
                    users_match.append(user_obj)

           response = {
            
            "match": users_match,
            "lasted_query":pendulum.now(tz='Asia/Bangkok')
            }
      

        else:
            response = {
                "queryString":f"{query}",
                "match":[],
                "lasted_query":pendulum.now(tz='Asia/Bangkok')
            }
        return response

    @staticmethod
    def get_userData(token_data):
        response ={}
  
 
        result = UserMangement.userDocuments.find_one({"uuid":token_data['uuid']})

        count_projects = len(result["projects"])
        count_teams = len(result['teams'])

        response={
            "profileImage":result["profile_photo"],
            "email":result["email"],
            "projects":result["projects"],
            "count_teams":count_teams,
            "count_projects":count_projects,
            "uuid":result["uuid"],
            "username":result["username"],
            "role":result["role"],
            "teams":result["teams"],
            "message":"Success"
        }
        
                                                                
     
        return response

       