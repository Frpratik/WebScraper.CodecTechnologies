from apscheduler.schedulers.background import BackgroundScheduler
from .scraper import scrape_website
from .database import save_results

scheduler = BackgroundScheduler()

def scrape_periodic():
    predefined_urls = ["https://example.com", "https://example.org"]
    for url in predefined_urls:
        data = scrape_website(url)
        if data["success"]:
            save_results(url, data)

def start_scheduler():
    scheduler.add_job(scrape_periodic, "interval", hours=12)
    scheduler.start()
