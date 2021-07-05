import cv2, io
from PIL import Image, ImageGrab
import numpy as np
import uuid
from utils.Recorddata import Recorddata
import string
import random
from datetime import datetime

class LabelingTool:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore
    dataStore = Recorddata.datastore
    taskStore = Recorddata.taskStore

    @staticmethod
    def FindColor(image):
        colorPos = []
        edgePos = {}

        for x in range(1, image.size[0]):
            for y in range(1, image.size[1]):
                if image.getpixel((x, y)) == 255:
                    edgePos = {"x": x, "y": y}
                    colorPos.append(edgePos)
        return colorPos

    
    @staticmethod
    def divide_chunks(l, n):
      
    # looping till length l
        for i in range(0, len(l), n): 
            yield l[i:i + n]


    @staticmethod

    @staticmethod
    def autoEdgeDetection(
        image, filename, algorithm="canny", theshold1=50, theshold2=50
    ):

        image = Image.open(io.BytesIO(image))
        print(image.size)

        numpy_image = np.array(image)

        noise_removed = cv2.GaussianBlur(numpy_image, (3, 3), 0)

        if algorithm == "canny":

            edge = cv2.Canny(noise_removed, theshold1, theshold2)

        elif algorithm == "laplacian":

            edge = cv2.Laplacian(noise_removed, cv2.CV_64F)

        elif algorithm == "solbelx":
            edge = cv2.Sobel(noise_removed, cv2.CV_64F, 1, 0, ksize=5)  # x

        elif algorithm == "solbely":
            edge = cv2.Sobel(noise_removed, cv2.CV_64F, 0, 1, ksize=5)  # y

        processed_img = Image.fromarray(edge)

        edge2path = LabelingTool.FindColor(processed_img)

        processed_img.save(f"cache/{filename}")

        print("DONE")

        return edge2path

    @staticmethod
    def edit(project_id, dataset_id, file_id, token_data):

        result = LabelingTool.projectStore.find_one({"project_uuid": project_id})
        if result != None:
            for dataset in LabelingTool.projectStore.find(
                {"project_datasets": project_id}
            ):
                print(dataset)

    @staticmethod
    def get_tasks(task_id,token_data):
        responses={}
        tasks = LabelingTool.taskStore.aggregate([
            {
                '$match': {
                    'task_uuid': task_id,
                }
            }, {
                '$unwind': {
                    'path': '$task_queue'
                }
            }, {
                '$match': {
                    'task_queue.labeler_uuid': token_data['uuid']
                }
            }
        ])

        for task in tasks:
            _id = str(task['_id'])
            responses={
                "task": task['task_queue']['task']
            }
            return responses

    @staticmethod
    def getimage(task_id, queue_id, token_data):
        task = LabelingTool.taskStore.aggregate([
        {
            '$match': {
                'task_uuid': task_id}
        }, {
            '$unwind': {
                'path': '$task_queue'
            }
        }, {
            '$match': {
                'task_queue.labeler_uuid': token_data['uuid']
            }
        }, {
            '$project': {
                f'task_queue.task.{queue_id}': 1
            }
        }
        ])
        
        for image_ in task:
            image_data = image_['task_queue']['task']

            if queue_id in image_data:

                response = {
                    "image":image_data[queue_id]['image']
                }
            else:
                response={
                    "message":"not found"
                }
            return response
    @staticmethod
    def create_task(project_id, task_name, task_labelers, token, task_mode="divide",task_due_date="" ,task_desciption=''):
        response= {}
        total_data =[]
        task_queue=[]
        task_={}
        splited_task = {}
        task_uuid = str(uuid.uuid4())
        n_labelers = len(task_labelers)
    
        
        if LabelingTool.projectStore.find_one({"project_uuid":project_id}) !=None:
           results = LabelingTool.projectStore.aggregate([
                        {
                            '$match': {
                                'project_uuid': project_id
                            }
                        }, {
                            '$unwind': {
                                'path': '$project_datasets'
                            }
                        }, {
                            '$lookup': {
                                'from': 'datastore', 
                                'localField': 'project_datasets', 
                                'foreignField': 'dataset_uuid', 
                                'as': 'project_datasets.attached_dataset'
                            }
                        }, {
                            '$unwind': {
                                'path': '$project_datasets.attached_dataset'
                            }
                        }, {
                            '$group': {
                                '_id': '$_id', 
                                'project_datasets': {
                                    '$push': '$project_datasets'
                                }
                            }
                        }
                    ])
           for result in results:
                    # _id = str(result['_id'])
                    
                    for data in result['project_datasets']:
                        
                        for image in data['attached_dataset']['dataset_files']:
                            
                            total_data.append(image[0])
                
            
           if task_mode == "divide":
                
                split = round(len(total_data) / n_labelers)
                labels = list(LabelingTool.divide_chunks(total_data,split))
                

                for  n_tasks, labeler in zip(labels,task_labelers):
                    for task in n_tasks:
                        q_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 6))  
                        task_[q_id]={"image":task, "is_labeled":False}  
                    splited_task={
                        "total_drivied":len(task_),
                         "labeler_uuid":labeler,
                         "task":task_
                     }
                    task_queue.append(splited_task)  


                   
                response={
                     "message":"success",
                     "mode":task_mode,
                     "n_labelers":n_labelers,
                     "task_owner_uuid":token['uuid'],
                     "task_uuid": task_uuid ,
                     "task_queue":task_queue,
                     "project_uuid":project_id,
                     "project_created_time": datetime.now(),
                    "total_image":len(total_data)
                }

                LabelingTool.taskStore.insert_one({
                    "message":"success",
                     "mode":task_mode,
                     "n_labelers":n_labelers,
                     "task_owner_uuid":token['uuid'],
                     "task_uuid": task_uuid ,
                     "task_queue":task_queue,
                     "project_uuid":project_id,
                     "project_created_time": datetime.now(),
                    "total_image":len(total_data)
                })       

                LabelingTool.projectStore.find_one_and_update(
                {"project_uuid": project_id}, 
                {"$push": {"tasks": task_uuid}})
                
           elif task_mode=="parallel":
               
                for labeler in task_labelers:
                    for task in total_data:
                        q_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 6))  
                        task_[q_id]={"image":task, "is_labeled":False}  
                    splited_task={
                            
                            "labeler_uuid":labeler,
                            "task":task_
                        }
                    task_queue.append(splited_task) 
                    

                response= {
                    "message":"success",
                    "mode":task_mode,
                    "n_labelers":n_labelers ,
                    "task_owner_uuid":token['uuid'],
                    "project_created_time": datetime.now(),
                    "task_queue":task_queue,
                    "task_uuid": task_uuid,
                    "project_uuid":project_id
                }

                LabelingTool.taskStore.insert_one({
                    "message":"success",
                    "mode":task_mode,
                    "n_labelers":n_labelers ,
                    "task_owner_uuid":token['uuid'],
                    "project_created_time": datetime.now(),
                    "task_queue":task_queue,
                    "task_uuid": task_uuid,
                    "project_uuid":project_id
                })

                LabelingTool.projectStore.find_one_and_update(
                {"project_uuid": project_id}, 
                {"$push": {"tasks": task_uuid}})
                
        else:
            response={
                "message":"not-fround project",
                "project_uuid":project_id
            }
        return response