from discord import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init_driver() -> webdriver:

    # Configure headless instance of driver.
    options = Options()
    options.headless = True

    # Initialize driver to click button to activate widget.
    driver = webdriver.Chrome(options=options)

    return driver


class Bot(Client):

    driver: webdriver
    chat_active: bool
    chat_count: int

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.driver = init_driver()
        self.chat_active = False
        self.chat_count = 1
