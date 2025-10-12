from fastapi import APIRouter, File, UploadFile, Depends, Form, HTTPException
from service.fileService import save_upload_file
from service.userService import update_user_avatar
from service.tokenService import oauth2_scheme, get_current_user

router = APIRouter(prefix="/files", tags=["Files"])


async def upload_user_avatar(
    file: UploadFile = File(...),
    image_type: str = Form(...),
    token: str = Depends(oauth2_scheme),
):
    path = await save_upload_file(file, category="user", image_type=image_type)

    return {"message": "Avatar updated successfully", "avatar_path": path}
