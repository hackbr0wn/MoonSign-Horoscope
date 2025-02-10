import aiohttp
import asyncio
from bs4 import BeautifulSoup

BASE_URL = "https://www.astroved.com"
MAX_CONCURRENT_REQUESTS = 5  # Limit to 5 concurrent requests at a time

async def fetch(session, url, timeout=10):
    """ Fetch page content asynchronously with a timeout """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    try:
        async with session.get(url, headers=headers, timeout=timeout) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None
    except asyncio.TimeoutError:
        return None  # Return None if there's a timeout
    except Exception as e:
        return None  # Return None for any other error

async def scrape_horoscope():
    """ Scrapes all horoscope links and their details asynchronously """
    url = f"{BASE_URL}/horoscope/"

    async with aiohttp.ClientSession() as session:
        page_content = await fetch(session, url)

        if not page_content:
            return {"error": "Failed to fetch main horoscope page"}

        soup = BeautifulSoup(page_content, "html.parser")

        # Extract all horoscope sign links
        horoscope_links = [a["href"] for a in soup.find_all("a", href=True) if "/horoscopes/daily-horoscope/" in a["href"]]

        # Use semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

        # Create tasks for concurrent fetching with concurrency limits
        tasks = [scrape_horoscope_details(session, semaphore, f"{BASE_URL}{link}", link.split("/")[-1].capitalize()) for link in horoscope_links]

        # Run tasks concurrently with a limit on concurrency
        results = await asyncio.gather(*tasks)

        return results

async def scrape_horoscope_details(session, semaphore, url, sign_name):
    """ Fetches detailed horoscope information asynchronously with concurrency limit """
    async with semaphore:
        page_content = await fetch(session, url)

        if not page_content:
            return {"sign": sign_name, "error": f"Failed to fetch {sign_name} horoscope"}

        soup = BeautifulSoup(page_content, "html.parser")
        
        horoscope_section = soup.find("div", class_="horo-title")

        if not horoscope_section:
            return {"sign": sign_name, "status": "fail", "message": "Horoscope section not found"}

        result = {"sign": sign_name, "horoscope": {}}

        headers = horoscope_section.find_all("h3")  
        descriptions = horoscope_section.find_all("p")  

        for header, description in zip(headers, descriptions):
            category = header.get_text(strip=True)  
            description_text = description.get_text(strip=True) 
            result["horoscope"][category] = description_text

        return result

