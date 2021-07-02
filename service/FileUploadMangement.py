from starlette import responses
import config as ENV
from fastapi import HTTPException
from datetime import datetime
from .TeamsMangement import TeamsMangement
from utils.Recorddata import Recorddata
import pendulum
from utils.FirebaseConnector import Firebase
import uuid
import random
from PIL import Image
import io




class FileUploadMangement:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore
    dataStore = Recorddata.datastore

    firebase_admin = Firebase()

    @staticmethod
    def UploadFile(files_content, dataset_name, dataset_uuid, files_name, token_data):

        fileUploadObj = {}

        datasetObj = []

        dataset = {}

        user_id = token_data["uuid"]
        file_uuid = str(uuid.uuid4())
        for filename, file_content in zip(files_name, files_content):


            im = Image.open(io.BytesIO(file_content))
            width, height = im.size
            # print(width,height)
            url = FileUploadMangement.firebase_admin.uploadUserFile(
                user_id,
                dataset_name,
                file_content,
                fileName=filename,
                filename_gen=file_uuid,
            )
            fileUploadObj = {
                "filename": filename,
                "file_url": url,
                "file_metadata":{
                    "width":width, 
                    "height":height
                },
                "uploader":user_id,
                "timestamp":datetime.now(),
                "file_uuid": file_uuid,
            }
            datasetObj.append(fileUploadObj)

        dataset = {
            "dataset_uuid": dataset_uuid,
            "dataset_name": dataset_name,
            "message": "Success",
            "content": datasetObj,
        }

        return dataset

    @staticmethod
    def CreateDataset(dataset_name, token_data, dataset_description=""):
        bg_list = [
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623682815/MD_NEX/cool-background_mg7zzn.png",
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623682815/MD_NEX/cool-background_2_erfmxs.png",
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623682815/MD_NEX/cool-background_1_jgyzpi.png",
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623910703/MD_NEX/cool-background_4_uyjgvu.png",
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623910705/MD_NEX/cool-background_3_piefpp.png",
            "https://res.cloudinary.com/image-chatbot/image/upload/v1623910705/MD_NEX/cool-background_3_piefpp.png",
        ]

        thumbnail_img = random.choice(bg_list)
        dataset_uuid = str(uuid.uuid4())
        dataset = {
            "dataset_name": dataset_name,
            "dataset_uuid": dataset_uuid,
            "dataset_thumbnail": thumbnail_img,
            "dataset_description": dataset_description,
            "dataset_owner_uuid": token_data["uuid"],
            "dataset_last_modified": datetime.now(),
            "dataset_created_time": datetime.now(),
            "dataset_files": [],
            "dataset_modified_log": {
                0: {
                    "name": token_data["issuer"],
                    "uuid": token_data["uuid"],
                    "action": "create_dataset",
                    "timestamp": datetime.now(),
                }
            },
            "message": "Dataset was created",
        }
        FileUploadMangement.dataStore.insert_one(
            {
                "dataset_name": dataset_name,
                "dataset_uuid": dataset_uuid,
                "dataset_description": dataset_description,
                "dataset_thumbnail": thumbnail_img,
                "dataset_owner_uuid": token_data["uuid"],
                "dataset_last_modified": datetime.now(),
                "dataset_created_time": datetime.now(),
                "dataset_files": [],
                "dataset_atteched_project": [],
                "dataset_modified_log": [
                    {
                        
                        "uuid": token_data["uuid"],
                        "action": "create_dataset",
                        "timestamp": datetime.now(),
                    }
                ],
                "dataset_members": [
                    {
                      
                        "uuid": token_data["uuid"],
                        "role": "dataset_owner",
                        "timestamp":datetime.now(),
                    }
                ],
                "isDeactive": False,
            }
        )

        return dataset

    @staticmethod
    def UpdateDataset(
        action_type,
        token_data,
        dataset_name,
        dataset_uuid,
        content=[],
        dataset_thumnail_url="",
        dataset_description="",
    ):
        response = {}
        if action_type == "UPDATE_FILES":
            FileUploadMangement.dataStore.find_one_and_update(
                {"dataset_uuid": dataset_uuid}, {"$push": {"dataset_files": content}}
            )
            response = {"message": "File Updated"}
        elif action_type == "UPDATE_THUMBNAIL":
            FileUploadMangement.dataStore.find_one_and_update(
                {"dataset_uuid": dataset_uuid},
                {"$push": {"dataset_thumbnail": content}},
            )
            response = {"message": "Thumbnail updated"}
        return response

    @staticmethod
    def check_owner(project_uuid):
        try:
            project_data = FileUploadMangement.projectStore.find_one(
                {"project_uuid": project_uuid}
            )
            project_owner = project_data["project_owner_uuid"]

        except:
            project_owner = None

        return project_owner

    @staticmethod
    def AddDatasetToProject(project_uuid, dataset_uuid, token_data):

        uuid_key = token_data["uuid"]
        owner = FileUploadMangement.check_owner(project_uuid)

        if owner == uuid_key:

            FileUploadMangement.projectStore.find_one_and_update(
                {"project_uuid": project_uuid},
                {"$push": {"project_datasets": dataset_uuid}},
            )
            FileUploadMangement.dataStore.find_one_and_update(
                {"dataset_uuid": dataset_uuid},
                {"$push": {"dataset_atteched_project": project_uuid}},
            )
            response = {"message": "dataset added to project"}
            return response

        else:
            raise HTTPException(
                status_code=401, detail="only project owner can add datset to project"
            )

    @staticmethod
    def RemoveDatasetToProject(project_uuid, dataset_uuid, token_data):

        uuid_key = token_data["uuid"]
        owner = FileUploadMangement.check_owner(project_uuid)

        if owner == uuid_key:
            FileUploadMangement.projectStore.find_one_and_update(
                {"project_uuid": project_uuid},
                {"$pull": {"project_datasets": dataset_uuid}},
            )
            FileUploadMangement.dataStore.find_one_and_update(
                {"dataset_uuid": dataset_uuid},
                {"$pull": {"dataset_atteched_project": project_uuid}},
            )
            response = {"message": "dataset removed to project"}
            return response

        else:
            raise HTTPException(
                status_code=401,
                detail="only project owner can remove datset to project",
            )

