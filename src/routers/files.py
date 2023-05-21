from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import shutil

files_router = APIRouter(prefix="/file", tags=["files"])


# только для текстового файла txt
@files_router.post("/file")
def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"lines": lines}


# загрузка файлов  и медиа
@files_router.post("/uploadfile")
def get_upload_file(upload_file: UploadFile = File(...)):
    path = f"media/{upload_file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return {"filename": path, "type": upload_file.content_type}


# для скачивания файлов
@files_router.get("/download/{name}", response_class=FileResponse)
def get_file(name: str):
    path = f"media/{name}"
    return path
