from fastapi import FastAPI, HTTPException, Query
import uvicorn
import json
import re
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup

app = FastAPI(
    title="Web Crawler API",
    description="API for crawling websites using crawl4ai",
    version="0.1.0"
)

@app.get("/crawl")
async def crawl_website(query: str = Query(..., description="Search query to crawl")):
    try:
        # Configure browser and crawler
        browser_config = BrowserConfig()
        run_config = CrawlerRunConfig()
        
        # Construct the URL with the query parameter
        url = f"https://www.verif.com/back-api/search?query={query}&isoCode=TN&startYear=1900-2025&resultType=organization&pageNumber=1&sortOrder=score&locale=en"
        
        # Execute the crawl
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(
                url=url,
                config=run_config
            )
                        
            # Use BeautifulSoup to extract the text inside the <pre> tag
            soup = BeautifulSoup(result.cleaned_html, "html.parser")
            pre_text = soup.find("pre").get_text()

            # Parse the extracted text as JSON
            data = json.loads(pre_text)
            
            return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crawling failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Web Crawler API. Use the /crawl endpoint to crawl websites."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
