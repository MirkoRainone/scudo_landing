from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# 1. Creiamo il router visivo
router = APIRouter(tags=["Pagine Web"])

# 2. Diciamo a FastAPI dove trovare la cartella con i file HTML
templates = Jinja2Templates(directory="templates")

# 3. La rotta per la Home Page ("/")
@router.get("/", response_class=HTMLResponse)
async def mostra_landing(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")