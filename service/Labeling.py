import cv2, io
from PIL import Image, ImageGrab
import numpy as np


class LabelingTool:
    @staticmethod
    def FindColor(image, color):
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

        edge2path = LabelingTool.FindColor(processed_img, (255, 255, 255))

        processed_img.save(f"cache/{filename}")

        print("DONE")

        return edge2path
