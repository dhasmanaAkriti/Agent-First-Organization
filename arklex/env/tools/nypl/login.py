from typing import Any, Dict
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

from agentorg.env.tools.tools import register_tool

description = "Allow the user to log in to the bknyl website to issue books"
slots = [
    {
        "name": "pin",
        "type": "string",
        "description": "The pin of the user or the barcode on the library card such as 'something@example.com'.",
        "prompt": "In order to proceed, please provide the barcode on the library card for identity verification.",
        "required": True,
    },
    {
        "name": "password",
        "type": "string",
        "description": "The password of the user to log into the account.",
        "prompt": "In order to proceed, please provide the pin code password for identity verification.",
        "required": True,
    }
]
outputs = [
    {
        "name": "successful log in",
        "type": "string",
        "description": "logged in successfully",
    }
]

@register_tool(description, slots, outputs)
def login_bknyl(pin, password, **kwargs) -> str:
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Open the web page
        driver.get("https://discover.bklynlibrary.org/my-account")

        # Find the username and password fields and enter the credentials
        username_field = driver.find_element(By.NAME, "my-account-login-barcode")
        password_field = driver.find_element(By.NAME, "my-account-login-pin")

        username_field.send_keys(pin)
        password_field.send_keys(password)

        # Find the login button and click it
        login_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Log In']")
        login_button.click()

        # Wait for the page to load and check for a successful login
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear

        # Check for an element that is only present after a successful login
        try:
            driver.find_element(By.NAME, "logout")  # Replace with the actual element name or ID
            return "logged in successfully"
        except NoSuchElementException:
            return "login failed"

    finally:
        # Close the browser
        driver.quit()