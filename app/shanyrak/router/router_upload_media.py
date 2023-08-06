from ..service import Service, get_service
from fastapi import Response, UploadFile, Depends
from . import router

@router.post("/shanyraks/{id:str}/media")
def updload_file_id(
    id : str,
    file : list[UploadFile],
    svc : Service = Depends(get_service)
):
    arrstr = []
    for f in file:
        arrstr.append(svc.s3_service.upload_file(f.file, f.filename))
    svc.repository.add_image_shanyrak(id, arrstr)
    return Response(status_code=200)