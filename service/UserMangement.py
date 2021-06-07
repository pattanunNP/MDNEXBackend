
from starlette import responses
import config as ENV
from fastapi import HTTPException
from utils.Recorddata import  Recorddata
import uuid
import pendulum



class UserMangemnet:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore


    
    @staticmethod
    def search_user(query, token_data):
        response ={}
        users_match ={}

        if query != None:
            
           for i,user in enumerate(UserMangemnet.userDocuments.find({"username":{"$regex":f"{query}",
                                                                                "$options":"i"}}).limit(100)):
               if user["uuid"] != token_data["uuid"]:                                                          
                    user_obj ={
                        "_id":str(user["_id"]),
                        "email":user["email"],
                        "uuid":user["uuid"],
                        "username":user["username"]}
                    users_match[i] = user_obj

           response = {
            "queryString":f"{query}",
            "match": users_match,
            "lasted_query":pendulum.now(tz='Asia/Bangkok')
            }
      

        else:
            response = {
                "message":"empty"
            }
        return response

       