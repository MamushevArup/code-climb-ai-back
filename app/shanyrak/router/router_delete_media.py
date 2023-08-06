from fastapi import Depends, Response

from ..service import Service, get_service
from . import router

@router.delete("/shanyraks/{id:str}/media")
def delete_media(
    house_id:str,
    svc: Service = Depends(get_service),
):
    medi = svc.repository.show_option(house_id)
    filenames = [url.split('/')[-1] for url in medi["media"]]
    for f in filenames:
        svc.s3_service.delete_file(f)
    print(medi)
    svc.repository.delete_media(house_id)
    return Response(status_code=200)