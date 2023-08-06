from . import router
@router.get("/ap")
def get_ap():
    return {"Hello": "From backend"}