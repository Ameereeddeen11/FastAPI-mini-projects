from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

template = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return template.TemplateResponse("main.html", {"request": request})

