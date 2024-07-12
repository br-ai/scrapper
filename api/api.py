from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def get_form():
    with open("form.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)