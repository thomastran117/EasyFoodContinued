import filetype, secrets, io
from pathlib import Path
from PIL import Image
from fastapi import UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from service.tokenService import require_auth_token, get_current_user

UPLOAD_DIR = Path("uploads/users")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 10 * 1024 * 1024


async def upload_user_avatar(
    file: UploadFile = File(...),
    token: str = Depends(require_auth_token),
):
    user = get_current_user(token)
    if not user:
        raise HTTPException(401, "Invalid user token")

    data = await file.read()
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(413, f"File exceeds {MAX_FILE_SIZE / (1024**2)} MB limit")

    kind = filetype.guess(data)
    if not kind or kind.mime not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, "Only JPG and PNG files are allowed")

    try:
        img = Image.open(io.BytesIO(data))
        img.verify()
    except Exception:
        raise HTTPException(400, "Corrupted or invalid image file")

    filename = f"{secrets.token_hex(16)}.{kind.extension}"
    path = UPLOAD_DIR / filename
    with open(path, "wb") as f:
        f.write(data)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Avatar uploaded successfully", "path": str(path)},
    )
