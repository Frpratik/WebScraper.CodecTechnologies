from fastapi import FastAPI, Form, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.background import BackgroundTasks
from fastapi.encoders import jsonable_encoder
import json
import pandas as pd

# Import custom modules
from app.scraper import scrape_website
from app.database import get_db, save_results, get_results, delete_result
from app.scheduler import start_scheduler

# Initialize FastAPI app
app = FastAPI()

# Configure templates and static files
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Start the scheduler
start_scheduler()

# Home route to render the homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the homepage."""
    return templates.TemplateResponse("index.html", {"request": request})


# Scrape data from provided URL and return it as JSON
@app.post("/scrape")
async def scrape(request: Request, url: str = Form(...), db=Depends(get_db)):
    """Scrape data from the provided URL and return it as JSON."""
    try:
        # Check if the URL format is valid
        if not url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="Invalid URL format.")
        
        # Perform scraping
        data = scrape_website(url)
        
        # If scraping failed, raise an exception
        if not data.get("success"):
            raise HTTPException(status_code=500, detail="Scraping failed.")
        
        # Optionally, save the scraped data to the database
        saved_data = save_results(url, data, db)
        
        # Serialize the response data using jsonable_encoder
        serialized_data = jsonable_encoder({
            "success": True,
            "data": data,
            "saved_data": saved_data
        })

        return JSONResponse(content=serialized_data)
    
    except Exception as e:
        # Return an error message if an exception occurs
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


# Retrieve saved scraping results from the database
@app.get("/saved_results", response_class=JSONResponse)
async def saved_results(db=Depends(get_db)):
    """Retrieve saved scraping results."""
    try:
        results = get_results(db)
        # Format results for the response
        formatted_results = [
            {"id": r.id, "url": r.url, "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")} 
            for r in results
        ]
        return {"success": True, "saved_results": formatted_results}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# Download scraped data as a JSON file
@app.post("/download/json")
async def download_json(background_tasks: BackgroundTasks, url: str = Form(...)):
    """Download scraped data as a JSON file."""
    try:
        data = scrape_website(url)
        file_path = "output.json"
        
        # Save data to a JSON file
        with open(file_path, "w") as f:
            json.dump(data, f)
        
        # Return the file as a response
        return FileResponse(file_path, filename="scraped_data.json")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Download scraped data as a CSV file
@app.post("/download/csv")
async def download_csv(background_tasks: BackgroundTasks, url: str = Form(...)):
    """Download scraped data as a CSV file."""
    try:
        data = scrape_website(url)
        
        # Assuming the data contains a list of titles to be saved in the CSV
        df = pd.DataFrame(data["titles"], columns=["Titles"])
        file_path = "output.csv"
        
        # Save data to a CSV file
        df.to_csv(file_path, index=False)
        
        # Return the file as a response
        return FileResponse(file_path, filename="scraped_data.csv")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete a saved scraping result by ID
@app.post("/delete", response_class=JSONResponse)
async def delete_scraped_result(id: int = Form(...), db=Depends(get_db)):
    """Delete a saved scraping result by ID."""
    try:
        result = delete_result(id, db)
        return {"success": True, "message": result["message"]}
    
    except Exception as e:
        return {"success": False, "message": str(e)}
