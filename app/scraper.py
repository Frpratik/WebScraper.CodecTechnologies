import requests
from bs4 import BeautifulSoup

def scrape_website(url, tags=None):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if not tags:
            tags = ["h1", "h2", "h3"]
        data = {
            "titles": [tag.text.strip() for t in tags for tag in soup.find_all(t)],
            "links": [a["href"] for a in soup.find_all("a", href=True)],
            "images": [img["src"] for img in soup.find_all("img", src=True)],
        }
        return {"success": True, **data}
    except Exception as e:
        return {"success": False, "error": str(e)}
