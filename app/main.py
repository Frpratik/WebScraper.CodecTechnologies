# main.py (FastAPI Routes)
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from .scraper import scrape_website
from .database import get_db, save_results, get_results, delete_result
from .scheduler import start_scheduler
import json

app = FastAPI()

# Static files and templates
templates = Jinja2Templates(directory="app/templates")

# Start the background scheduler
start_scheduler()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scrape", response_class=HTMLResponse)
async def scrape(request: Request, url: str = Form(...), db=Depends(get_db)):
    data = scrape_website(url)
    if data["success"]:
        saved_data = save_results(url, data, db)
    return templates.TemplateResponse("index.html", {"request": request, "data": data, "url": url, "saved_data": saved_data})

@app.get("/results", response_class=HTMLResponse)
async def view_results(request: Request, db=Depends(get_db)):
    results = get_results(db)
    return templates.TemplateResponse("index.html", {"request": request, "saved_results": results})

@app.post("/download/json")
async def download_json(url: str = Form(...)):
    data = scrape_website(url)
    file_path = "output.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return FileResponse(file_path, filename="scraped_data.json")

@app.post("/download/csv")
async def download_csv(url: str = Form(...)):
    data = scrape_website(url)
    import pandas as pd
    df = pd.DataFrame(data["titles"], columns=["Titles"])
    file_path = "output.csv"
    df.to_csv(file_path, index=False)
    return FileResponse(file_path, filename="scraped_data.csv")

@app.post("/delete")
async def delete_scraped_result(id: int = Form(...), db=Depends(get_db)):
    result = delete_result(id, db)
    return JSONResponse(content={"success": True, "message": result["message"]})
