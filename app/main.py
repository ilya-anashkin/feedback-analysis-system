from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.feedback_routes import router as feedback_router

app = FastAPI()

app.include_router(feedback_router, prefix="/api/feedback")

app.mount("/docs", StaticFiles(directory="app/docs"), name="docs")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/docs/index.html", response_class=HTMLResponse)
async def read_index():
    """
    Serve the index.html file located in the app/docs directory.

    This endpoint reads the contents of the index.html file and
    returns it as an HTML response. This allows users to access
    the documentation directly through the API.

    Returns:
        HTMLResponse: The contents of the index.html file with
                      a status code of 200 (OK).

    Raises:
        FileNotFoundError: If the index.html file does not exist,
                           the server will raise an exception.
    """
    return HTMLResponse(content=open("app/docs/index.html").read(), status_code=200)
