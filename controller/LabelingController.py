from typing import Optional, List
from service.Labeling import LabelingTool
from service.AuthenticationMangement import Authentication
from fastapi import APIRouter, Header, File, UploadFile
from fastapi.responses import FileResponse

labeling_control_api = APIRouter()


# acess controller
@labeling_control_api.post("/labeling/auto-edgedetection")
async def search_user(
    theshold1: Optional[int],
    theshold2: Optional[int],
    algorithm: Optional[str],
    Image: UploadFile = File(...),
    Authorization: Optional[str] = Header(None),
):

    """
    เป็น API สำหรับการ Search User
    Parameters
    ----------
    data : pydantic
    * username  : str
  
    
    Returns
    -------
    username, email, uuid

    """
    filename = Image.filename

    file_content = await Image.read()

    Authentication.verify_token(Authorization)

    result = LabelingTool.autoEdgeDetection(
        file_content, filename, algorithm, theshold1, theshold2
    )

    return result

