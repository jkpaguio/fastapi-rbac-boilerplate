# app/routes/files.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from ..lib import s3_files
from ..lib import branca_token
from typing import List
import os

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    codes = []
    for file in files:
        temp_file_path = os.path.join("tmp", file.filename)
        
        # Save file to temporary folder
        with open(temp_file_path, "wb") as buffer:
            file_content = file.file.read()
            buffer.write(file_content)

        # Upload file to S3
        s3_files.upload_to_s3(file.filename, file_content)

        # Delete the temporary file
        os.remove(temp_file_path)

        # Generate pybranca code
        code = branca_token.encode_branca(file.filename)
        codes.append({"filename": file.filename, "code": code})

    # Return array of pybranca codes
    return codes
    
@router.get("/get_file_from")
async def get_file_from_folder(folder: str = ""):
    file = s3_files.get_one_file_in_bucket(folder)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"file": file}    
    
@router.get("/get_signed_url")
async def get_file_from_folder(file: str = ""):
    """
    Get Signed Url for file
    """
    file = s3_files.generate_presigned_url(file)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"file": file}    


@router.get("/test_move_file")
async def test_move_file():
    old_file_key = s3_files.get_one_file_in_bucket("")
    new_file_key = f"new_folder/{old_file_key}"
    s3_files.move_file_in_bucket(old_file_key, new_file_key)
    return {"message": "File moved successfully"}