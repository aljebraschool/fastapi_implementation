from pydantic import BaseModel

class FileResponse(BaseModel):
    filename : str
    content_type : str
    file_size : int

class MultipleFileResponse(BaseModel):
    files : list[FileResponse]
