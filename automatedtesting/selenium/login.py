# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import datetime


def timestamp():
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (ts + '\t')

# Start the browser and login with standard_user
def login (user, password):
    print (timestamp() + 'Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless") 
    driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    print (timestamp() + 'Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')

    # login
    print(timestamp() + 'Try to login in with {} {}'.format(user, password))
    driver.find_element_by_css_selector("input[id='user-name']").send_keys(user)
    driver.find_element_by_css_selector("input[id='password']").send_keys(password)
    driver.find_element_by_id("login-button").click()

    # login test
    product_text = driver.find_element_by_css_selector("div[id='header_container'] > div.header_secondary_container > span").text
    assert "PRODUCTS" in product_text 
    
    print(timestamp() + 'Succesfull login in with {} {}'.format(user, password))

    return driver

def add_to_cart(driver):

    article_count = 0

    num_articles = len(driver.find_elements_by_class_name("inventory_item"))
    for article in driver.find_elements_by_class_name("inventory_item"):
        article_name = article.find_element_by_css_selector("div.inventory_item_name").text

        article.find_element_by_css_selector("div.pricebar > button").click()

        number = driver.find_element_by_css_selector("span.shopping_cart_badge").text

        article_count += 1
        assert article_count == int(number)

        print(timestamp() + 'Added to cart {} item {}/{}'.format(article_name, number, num_articles))


def remove_from_cart(driver):
    
    
    num_articles = len(driver.find_elements_by_class_name("inventory_item"))
    article_count = num_articles
    for article in driver.find_elements_by_class_name("inventory_item"):
        number = driver.find_element_by_css_selector("span.shopping_cart_badge").text
        assert article_count == int(number)
        article_count -= 1

        article_name = article.find_element_by_css_selector("div.inventory_item_name").text

        article.find_element_by_css_selector("div.pricebar > button").click()

        print(timestamp() + 'Removed from cart {} item {}/{}'.format(article_name, number, num_articles))

if __name__ == "__main__":
    driver = login('standard_user', 'secret_sauce')

    add_to_cart(driver)

    remove_from_cart(driver)

    print(timestamp() + 'All tests successful')

