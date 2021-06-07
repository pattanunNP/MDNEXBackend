import config as ENV
import jwt
from fastapi import HTTPException, responses
from datetime import datetime,timedelta
import bcrypt
from database.MongoDBConnector import MongoConnector
import uuid
from pymongo import TEXT
import requests
import pendulum

"""
There are lines for checking token from user 
"""

class Authentication:

    db = MongoConnector.connect()
    userDB = db.usersdata
    userDocuments = db.userdocuments
    
    @staticmethod
    def verify_token(x_token):
        x_token = x_token.split("Bearer")[-1]
        
        jwt_options = {'verify_signature': False, 'verify_exp': True}
        if len(x_token) !=0:
            try:
                data = jwt.decode(x_token, ENV.SECERET_KEY, algorithms=['HS256'], options=jwt_options)
                return x_token,data

            except Exception as err:
                raise HTTPException(status_code=403, detail="X-Token invalid")
                
        else:
            raise HTTPException(status_code=401, detail="Missing X-Token")
        
    
    @staticmethod
    def login(username, password, timeout=5):
        
        user_check = [user for user in Authentication.userDB.find({"username":username})]
   
        
        if len(user_check) == 1:

            hashed_password = str(user_check[0]['password']).encode()
            isVerified = user_check[0]['isVerified']
            uuid_key = user_check[0]['uuid']
            query_password = password.encode()
            

            if isVerified == True:
                if bcrypt.checkpw(query_password,hashed_password):
                    payload = {
                        "name":username,
                        "uuid":uuid_key,
                        "exp": datetime.utcnow() + timedelta(days=timeout)
                    }
                    token = jwt.encode(payload, ENV.SECERET_KEY)

                    respone = {

                        "uuid":uuid_key,
                        "exp":f"{timeout} days",
                        "token":token
                    }

                    return respone
                    
                else:
                    respone = {
                        "message":"Invild password"
                    }
                    return respone
            else:
                respone = {
                    "message":"Please verify email first !"
                }
                return respone
        else:
            respone = {
                "message":"Couldn't found username"
            }
            return respone


    @staticmethod
    def generate_confrim_email(email, uuid_key, timeout):
        payload = {
                    "email":email,
                    "uuid":uuid_key,
                    "exp": datetime.utcnow() + timedelta(minutes=timeout)
                }
        confrim_email_token  = jwt.encode(payload,
                                    ENV.SECERET_EMAIL_KEY)

        return confrim_email_token

    @staticmethod
    def send_verify_email(username, email, uuid_key, timeout=10):

        confrim_email_token = Authentication.generate_confrim_email(email, uuid_key,timeout)
        confrim_email_link = f"{ENV.ROOT_URL}/api/v1/confrim/email?verify_token={confrim_email_token}"

        r = requests.post(
            "https://api.mailgun.net/v3/mg.standupcode.co/messages",
            auth=("api", f"{ENV.MAILGUN_API_KEY}"),
            data={"from": f"MDNEX Support Admin <{ENV.MAILGUN_DOMAIN}>",
                "to": f"{username} <{email}>",
                "subject": "Verify Your Account",
                "template": "verify_email",
                "v:verify_link":f"{confrim_email_link}"
                }
            )
        print(f"Sending email...{email}")
        print(r.status_code)
        print(r.text)
        response ={
            "message":f"Verification link was sent to {email} link will expire in {timeout} minutes "
        }
        print(confrim_email_link)
        return response
        

    @staticmethod
    def register(username, email, password):
        
        #check email
        email_check = [email for email in Authentication.userDB.find({"email":email})]
        user_check = [user for user in Authentication.userDB.find({"username":username})]

        if len(email_check) >= 1 :
            respone ={
                "message":"email already exists"
            }
            raise HTTPException(status_code=409, detail=respone)

        elif len(user_check)>=1:
             respone ={ "message":"username already exists"}
             raise HTTPException(status_code=409, detail=respone)
            

        else:
                       
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            user_id = str(uuid.uuid4())
            
           
            respone = {
                "email":email,
                "username":username,
                "password": hashed_password,
                "uuid":user_id,
                "message":"user created"
            
            
            }
            #insert data to db
            Authentication.userDB.insert_one({
                "email":email,
                "username":username,
                "password": hashed_password,
                "uuid":user_id,
                "registedTime":pendulum.now(tz='Asia/Bangkok'),
                "isVerified":False,
                "verifiedTime":""
                
            })

            Authentication.userDocuments.insert_one({
                "email":email,
                "username":username,
                "profile_photo":"https://image.flaticon.com/icons/png/512/149/149071.png",
                "uuid":user_id,
                "role":"",
                "projects":[], 
                "teams":[]
            })


            return respone


    @staticmethod
    def check_verify_email(uuid_key):
        result = Authentication.userDB.find_one({"uuid":uuid_key})
        
        response = {
            "username":result["username"],
            "email":result["email"],
            "isVerified":bool(result['isVerified']),
            "verifiedTime":result['verifiedTime']
        }
        return response

    @staticmethod
    def confrim_email(verify_token):
     

        jwt_options = {'verify_signature': False, 'verify_exp': True}
        if len(verify_token) !=0:
            try:
                data = jwt.decode(verify_token, ENV.SECERET_EMAIL_KEY, algorithms=['HS256'], options=jwt_options)
                
                response = {"message":"account_verified",
                            "uuid":data['uuid']}
                Authentication.userDB.find_one_and_update(
                    {"uuid":data['uuid']},
                    {"$set":{"isVerified":True,
                            "verifiedTime":str(pendulum.now(tz='Asia/Bangkok'))}}
                )
                return response

            except Exception as err:
                raise HTTPException(status_code=403, detail="X-Token invalid")
                
        else:
            raise HTTPException(status_code=401, detail="Missing X-Token")
