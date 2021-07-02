import cv2, io
from PIL import Image, ImageGrab
import numpy as np
from utils.Recorddata import Recorddata


class LabelingTool:

    userDocuments = Recorddata.userDocuments
    projectStore = Recorddata.projectStore
    teamStore = Recorddata.teamStore
    dataStore = Recorddata.datastore

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
    def getimage(project_id, dataset_id, file_id, token_data):
        for files in LabelingTool.dataStore.find({"dataset_uuid": dataset_id}):
            for file in files["dataset_files"]:
                if file[0]["file_uuid"] == file_id:
                    return file[0]

    @staticmethod
    def create_task(project_id,token_data,spec_user="All"):

        if spec_user == "All":
            
            for dataset in LabelingTool.projectStore({"project_uuid": project_id}):
                print(dataset["data"])


        return