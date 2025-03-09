from typing import Any, Dict
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

from agentorg.env.tools.tools import register_tool

description = "Allow the user to search for books on the bknyl website"

slots = [
    {
        "name": "query",
        "type": "string",
        "description": "The search query for finding books.",
        "prompt": "Could you please provide me the name of the book you want to look for?",
        "required": True,
    }
]

outputs = [
    {
        "name": "results",
        "type": "list",
        "description": "A list of search results with book titles and links.",
    }
]

@register_tool(desc=description, slots=slots, outputs=outputs)
def search_books(query: str, **kwargs) -> Dict[str, Any]:
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open the search page
        driver.get("https://discover.bklynlibrary.org/")

        # Find the search input field and enter the query
        search_field = driver.find_element(By.NAME, "searchTerm")
        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)

        # Wait for the search results to load
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

        # Collect the search results
        results = []
        try:
            book_elements = driver.find_elements(By.CSS_SELECTOR, ".search-result-item")  # Adjust the selector as needed
            for book in book_elements:
                title_element = book.find_element(By.CSS_SELECTOR, ".title")  # Adjust the selector as needed
                link_element = book.find_element(By.CSS_SELECTOR, "a")  # Adjust the selector as needed
                results.append({
                    "title": title_element.text,
                    "link": link_element.get_attribute("href")
                })
        except NoSuchElementException:
            return {"results": []}

        return {"results": results}

    finally:
        # Close the browser
        driver.quit()