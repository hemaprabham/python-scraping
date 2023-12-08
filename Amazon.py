import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

def init_driver():
    # Initialize the Selenium webdriver (you may need to specify the path to your webdriver executable)
    driver = webdriver.Chrome()
    return driver

def scrape_amazon_products(url):
    # Initialize the webdriver
    driver = init_driver()
    
    # Open the URL
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load

    # Scroll down to load more products (you may need to adjust this based on the website)
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Get the HTML content after scrolling
    page_source = driver.page_source

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all product containers on the page
    product_containers = soup.find_all('div', class_='s-result-item')

    product_data = []
    for container in product_containers:
        # Extract product details
        product_name = container.find('span', class_='a-text-normal').text.strip()
        try:
            price = container.find('span', class_='a-offscreen').text.strip()
        except AttributeError:
            price = 'N/A'  # Handle the case where price is not available

        try:
            rating = container.find('span', class_='a-icon-alt').text.strip()
        except AttributeError:
            rating = 'N/A'  # Handle the case where rating is not available

        try:
            seller_name = container.find('div', class_='a-row a-size-base a-color-secondary').text.strip()
        except AttributeError:
            seller_name = 'N/A'  # Handle the case where seller name is not available

        # Check if the product is out of stock
        out_of_stock = 'Currently unavailable' in container.get_text()

        if not out_of_stock:
            product_data.append([product_name, price, rating, seller_name])

    # Close the webdriver
    driver.quit()

    return product_data

def write_to_csv(data, filename='amazon_products.csv'):
    # Write the data to a CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Write header
        csv_writer.writerow(['Product Name', 'Price', 'Rating', 'Seller Name'])
        # Write data
        csv_writer.writerows(data)

if __name__ == "__main__":
    # Specify the URL of the Amazon page
    amazon_url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

    # Scrape product details
    product_data = scrape_amazon_products(amazon_url)

    # Write data to CSV
    write_to_csv(product_data)
