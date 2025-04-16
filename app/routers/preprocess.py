# app/routers/preprocess.py

from fastapi import APIRouter, UploadFile, File
from app.utils.file_loader import preprocess_case
import tempfile

router = APIRouter()

@router.post("/upload")
async def upload_case(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    result = preprocess_case(tmp_path)
    return result
