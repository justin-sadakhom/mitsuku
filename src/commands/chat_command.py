from typing import List

from selenium.common.exceptions import NoSuchElementException

from bot import Bot

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

URL = 'https://chat.kuki.ai/'


def setup(driver: webdriver) -> None:
    """Set up the web page that's to be scraped."""

    # Find and click buttons to activate chat window.
    driver.get(URL)

    button = driver.find_elements_by_class_name('pb-quickReply')[1]
    button.click()

    button = driver.find_elements_by_class_name('pb-quickReply')[2]
    button.click()

    button = driver.find_elements_by_class_name('pb-quickReply')[5]
    button.click()

    # Wait until input form is visible.
    WebDriverWait(driver, 10).until(
        ec.visibility_of_all_elements_located((By.ID, 'main-input'))
    )


def clean_input(text: str) -> str:
    if text.startswith('~chat'):
        return text[5:]

    return text


def chat(dialogue: str, driver: webdriver, count: int) -> List[str]:
    """Input dialogue for the chat bot and return their response."""

    # Locate chat form.
    chat_form = driver.find_element_by_xpath(
        "//div[@id='main-input']/input"
    )

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
            children = message.find_elements_by_xpath(
                ".//img[@class='pb-standalone-image pb-fullSizeImage']"
            )

            for child in children:
                response.append(child.get_attribute('src'))

        elif not has_button(message):
            response.append(message.text)

    return response


def has_image(element: WebElement) -> bool:
    """Return true iff this element doesn't have text,
    meaning it must be an image."""

    return element.text == ''


def has_button(element: WebElement) -> bool:
    """Return true iff this element has a button."""

    try:
        element.find_element_by_class_name('pb-buttonList__container')
    except NoSuchElementException:
        return False

    return True


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
