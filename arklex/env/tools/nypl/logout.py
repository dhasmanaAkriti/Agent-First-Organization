from typing import Any, Dict
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

from agentorg.env.tools.tools import register_tool

description = "Allow the user to log out of the bknyl website"


@register_tool(desc="Log out from the bknyl website", slots=[], outputs=[])
def logout_bknyl(**kwargs) -> str:
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open the web page
        driver.get("https://discover.bklynlibrary.org/my-account")

        # Wait for the page to load and check for the logout button
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

        # Find the logout button and click it
        try:
            logout_button = driver.find_element(By.NAME, "logout")  # Replace with the actual element name or ID
            logout_button.click()
            return "logged out successfully"
        except NoSuchElementException:
            return "logout failed"

    finally:
        # Close the browser
        driver.quit()