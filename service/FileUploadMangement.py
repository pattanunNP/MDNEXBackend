import config as ENV
from fastapi import HTTPException
from datetime import datetime
from .TeamsMangement import TeamsMangement
from utils.Recorddata import Recorddata


class FileUploadMangement:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore
    dataStore = Recorddata.datastore

    @staticmethod
    def UploadFile(files_content, files_name, token_data):

        fileUploadObj = {}

        filePack = []

        dataset = {}

        for filename, file_content in zip(files_name, files_content):

            fileUploadObj = {
                "filename": filename,
                #  "file_content": file_content
            }
            filePack.append(fileUploadObj)

        dataset = {"dataset_name": "test", "dataset_data": filePack}

        return dataset

