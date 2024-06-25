from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter()
router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/",response_class=HTMLResponse)
async def get():
    with open ("templates/test.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)