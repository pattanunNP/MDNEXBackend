import config as ENV
from fastapi import HTTPException
from datetime import datetime
from .TeamsMangement import TeamsMangement
from utils.Recorddata import Recorddata
import pendulum
from utils.FirebaseConnector import Firebase
import uuid


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

        for filename, file_content in zip(files_name, files_content):

            url = FileUploadMangement.firebase_admin.uploadUserFile(
                user_id, dataset_name, file_content, filename,
            )
            fileUploadObj = {
                "filename": filename,
                "files_url": url,
                "file_uuid": f"{uuid.uuid4()}",
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

        dataset_uuid = str(uuid.uuid4())
        dataset = {
            "dataset_name": dataset_name,
            "dataset_uuid": dataset_uuid,
            "dataset_thumbnail": "https://res.cloudinary.com/image-chatbot/image/upload/v1623645430/MD_NEX/Stand_Up_Code_y98un8.png",
            "dataset_description": dataset_description,
            "dataset_owner_uuid": token_data["uuid"],
            "dataset_owner_name": token_data["issuer"],
            "dataset_last_modified": str(pendulum.now(tz="Asia/Bangkok")),
            "dataset_created_time": str(pendulum.now(tz="Asia/Bangkok")),
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
                "dataset_owner_uuid": token_data["uuid"],
                "dataset_last_modified": pendulum.now(tz="Asia/Bangkok"),
                "dataset_created_time": pendulum.now(tz="Asia/Bangkok"),
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
