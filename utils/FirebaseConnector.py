import config as ENV
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


class Firebase:
    def __init__(self) -> None:

        cred = credentials.Certificate(ENV.FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(
            cred, {"storageBucket": "mdnex-projects.appspot.com"}
        )
        self.bucket = storage.bucket()
        print("Firebase: Connected !")

    def uploadUserFile(self, userID, datasetName, Data, fileName, filename_gen):
        ftype = fileName.split(".")[-1]

        blob = self.bucket.blob(
            f"Dataset/{userID}/{datasetName}/{filename_gen}.{ftype}"
        )
        try:
            blob.upload_from_string(Data, content_type="application/octet-stream")

            url = self.bucket.get_blob(
                f"Dataset/{userID}/{datasetName}/{filename_gen}.{ftype}"
            )
            url.make_public()
            return url.media_link
        except Exception as e:
            print(e)

