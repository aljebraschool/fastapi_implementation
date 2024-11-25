from http.client import HTTPException
from schemas.files import *
from fastapi import APIRouter, File, UploadFile

router = APIRouter(
    prefix="/files",
    tags=["files"]

)

@router.post("/upload", response_model= FileResponse)
def upload_file(file : UploadFile = File(...) ):

    try:
        content = file.file.read()

        file_size = len(content)

        # Reset file position after reading
        file.file.seek(0)

        return {
            "filename": file.filename,
            "file_size": file_size,
            "content_type": file.content_type

        }
    except Exception as e:
        raise HTTPException(status_code=405, detail=f"Error processing file {str(e)}")
    finally:
        file.close()

@router.post("/upload/multiple", response_model=MultipleFileResponse)
def upload_multiple_files(files: list[UploadFile] = File(...)):
    try:
        list_of_files = []

        for file in files:
            content = file.file.read()
            file_size = len(content)

            # Reset file position after reading
            file.file.seek(0)

            list_of_files.append({
                "filename": file.filename,
                "file_size": file_size,
                "content_type": file.content_type,  # Changed from "content-type" to "content_type"
            })

        return {"files": list_of_files}
    except Exception as e:
        raise HTTPException(status_code=408, detail=f"Error processing files {str(e)}")




