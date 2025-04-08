import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
import xmltodict
import json
from bs4 import BeautifulSoup

async def main():
    browser_config = BrowserConfig()  # Default browser configuration
    run_config = CrawlerRunConfig()   # Default crawl run configuration

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.verif.com/back-api/directSearch/search/?searchTerm=DJERBA&countryISOAlpha2Code=TN",
            config=run_config
        )
        html_data = result.cleaned_html  # Print clean markdown content
        
        # Use BeautifulSoup to extract XML content
        soup = BeautifulSoup(html_data, 'html.parser')
        xml_string = soup.find('searchresultdto').prettify()

        # Step 2: Convert XML to dictionary
        xml_dict = xmltodict.parse(xml_string)

        # Step 3: Convert dictionary to JSON
        json_output = json.dumps(xml_dict, indent=2)

        print(json_output)

if __name__ == "__main__":
    asyncio.run(main())