from typing import List
from bot import Bot

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://www.pandorabots.com/mitsuku/'


def setup(driver: webdriver) -> None:
    """Set up the web page that's to be scraped."""

    # Find and click button to activate chat window.
    driver.get(URL)
    button = driver.find_element_by_class_name('pb-widget__launcher')
    button.click()

    # Wait until input form is visible.
    WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.ID, 'pb-widget-input-form'))
    )


def clean_input(text: str) -> str:
    if text.startswith('~chat'):
        return text[5:]


def chat(dialogue: str, driver: webdriver, count: int) -> List[str]:
    """Input dialogue for the chat bot and return their response."""

    # Locate chat form.
    chat_form = driver.find_element_by_id('pb-widget-input-field')

    # Wait for chat window to load.
    WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located(
            (By.XPATH, "(//div[@class='pb-bot-response'])[1]")
        )
    )

    chat_form.send_keys(dialogue)
    chat_form.send_keys(Keys.RETURN)

    # Wait for response.
    WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located(
            (By.XPATH, "(//div[@class='pb-bot-response'])[" + str(count) + ']')
        )
    )

    # Get response and extract relevant text.
    messages = driver.find_element_by_xpath(
        "(//div[@class='pb-bot-response'])[" + str(count) + ']'
    ).find_elements_by_class_name('pb-message')

    response = []

    for message in messages:

        if has_image(message):
            children = message.find_elements_by_xpath('.//*')

            for child in children:
                response.append(child.get_attribute('src'))

        else:
            response.append(message.text)

    return response


def has_image(element: WebElement) -> bool:
    """Return true iff this element doesn't have text,
    meaning it must be an image."""

    return element.text == ''


if __name__ == '__main__':
    """EXAMPLE USAGE"""

    bot = Bot()
    setup(bot.driver)

    queue = ['Hello', 'Send a picture of bananas.', 'Tell me a story.']
    chat_count = 2

    while chat_count < 5:
        chat_input = queue[chat_count - 2]
        print(chat_input)
        print(chat(chat_input, bot.driver, chat_count))
        chat_count += 1
