import config as ENV
import firebase_admin
from firebase_admin import credentials


class Firebase:
    def __init__(self) -> None:

        cred = credentials.Certificate(ENV.FIREBASE_CRED_PATH)
        firebase_admin.initialize_app(
            cred, {"storageBucket": "gs://mdnex-projects.appspot.com/"}
        )
        print("Firebase: Connected !")
