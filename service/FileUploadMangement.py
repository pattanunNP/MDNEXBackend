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

            url = FileUploadMangement.firebase_admin.uploadUserFile(
                user_id,
                dataset_name,
                file_content,
                fileName=filename,
                filename_gen=file_uuid,
            )
            fileUploadObj = {
                "filename": filename,
                "files_url": url,
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
        ]

        thumbnail_img = random.choice(bg_list)
        dataset_uuid = str(uuid.uuid4())
        dataset = {
            "dataset_name": dataset_name,
            "dataset_uuid": dataset_uuid,
            "dataset_thumbnail": thumbnail_img,
            "dataset_description": dataset_description,
            "dataset_owner_uuid": token_data["uuid"],
            "dataset_owner_name": token_data["issuer"],
            "dataset_last_modified": str(pendulum.now(tz="Asia/Bangkok")),
            "dataset_created_time": str(pendulum.now(tz="Asia/Bangkok")),
            "dataset_files": [],
            "dataset_modified_log": {
                0: {
                    "name": token_data["issuer"],
                    "uuid": token_data["uuid"],
                    "action": "create_dataset",
                    "timestamp": str(pendulum.now(tz="Asia/Bangkok")),
                }
            },
            "message": "Dataset was created",
        }
        FileUploadMangement.dataStore.insert_one(
            {
                "dataset_name": dataset_name,
                "dataset_uuid": dataset_uuid,
                "dataset_description": dataset_description,
                "dataset_owner_name": token_data["issuer"],
                "dataset_thumbnail": thumbnail_img,
                "dataset_owner_uuid": token_data["uuid"],
                "dataset_last_modified": str(pendulum.now(tz="Asia/Bangkok")),
                "dataset_created_time": str(pendulum.now(tz="Asia/Bangkok")),
                "dataset_files": [],
                "dataset_modified_log": [
                    {
                        "name": token_data["issuer"],
                        "uuid": token_data["uuid"],
                        "action": "create_dataset",
                        "timestamp": pendulum.now(tz="Asia/Bangkok"),
                    }
                ],
                "dataset_members": [
                    {
                        "name": token_data["issuer"],
                        "uuid": token_data["uuid"],
                        "role": "dataset_owner",
                        "timestamp": pendulum.now(tz="Asia/Bangkok"),
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

