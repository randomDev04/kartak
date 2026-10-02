import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/upload", tags=["upload"])

## Ensure the upload directory exists
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

## Upload file endpoint
@router.post("/uploadFiles")
def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Check if filename not there in the upload directory
    if not filename:
        raise HTTPException(status_code=400, detail="File not selected for upload")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    return {
        "filename": filename,
        "message": "File uploaded successfully.",
        "file_url": f"/upload/files/{filename}"
        }

@router.get("/files/{filename}")
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)