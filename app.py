import config as ENV
from controller.AuthenticationController import acess_control_api
from controller.UserController import user_control_api
from controller.ProjectsController import projects_control_api
from controller.TeamsController import teams_control_api
from controller.FileUploadController import fileupload_control_api
from controller.LabelingController import labeling_control_api


from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI


app = FastAPI(title="MD NEX", description="API for MDNEX", version="0.1.0")

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://mdnex.netlify.app",
    "https://mdnex.standupcode.co",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Basic"], status_code=200)
def index():
    status = {"message": "MD NEX API V.0.1.0"}
    status = jsonable_encoder(status)
    return status


app.include_router(acess_control_api, prefix="/api/v1")
app.include_router(projects_control_api, prefix="/api/v1")
app.include_router(teams_control_api, prefix="/api/v1")
app.include_router(user_control_api, prefix="/api/v1")
app.include_router(fileupload_control_api, prefix="/api/v1")
app.include_router(labeling_control_api, prefix="/api/v1")
