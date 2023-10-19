import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to parse individual product page and extract information
def extract_product_info(product_url):
    response = requests.get(product_url)
    if response.status_code != 200:
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product_data = {}
    
    # Extract the required information (Description, ASIN, Product Description, Manufacturer)
    product_data['Description'] = soup.find('div', {'id': 'productDescription'}).get_text(strip=True) if soup.find('div', {'id': 'productDescription'}) else ''
    product_data['ASIN'] = soup.find('th', text='ASIN').find_next('td').text if soup.find('th', text='ASIN') else ''
    product_data['Product Description'] = soup.find('th', text='Product Dimensions').find_next('td').text if soup.find('th', text='Product Dimensions') else ''
    product_data['Manufacturer'] = soup.find('th', text='Manufacturer').find_next('td').text if soup.find('th', text='Manufacturer') else ''
    
    return product_data

# Read the Amazon HTML file and parse it using BeautifulSoup
with open('amazon20.html', 'r', encoding='utf-8') as file:
    amazon_html = file.read()

soup = BeautifulSoup(amazon_html, 'html.parser')

# Initialize lists to store data
product_urls = []
product_names = []
product_prices = []
ratings = []
reviews = []

# Find all product containers
product_containers = soup.find_all('div', class_='puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v3vtwxgppca0z12v18v51zrqona s-latency-cf-section s-card-border')

# Loop through product containers and extract the information
for container in product_containers:
    product_url = container.find('a', class_='a-link-normal')['href'] if container.find('a', class_='a-link-normal') else ''
    product_name = container.find('span', class_='a-size-medium a-color-base a-text-normal').text if container.find('span', class_='a-size-medium a-color-base a-text-normal') else ''
    product_price = container.find('span', class_='a-price-whole').text if container.find('span', class_='a-price-whole') else ''
    rating = container.find('i', class_='a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom').text if container.find('i', class_='a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom') else ''
    review = container.find('span', class_='a-size-base s-underline-text').text if container.find('span', class_='a-size-base s-underline-text') else ''
    
    # Extract additional product information by hitting the product URL
    product_data = extract_product_info(product_url)
    
    # Add extracted data to lists
    product_urls.append(product_url)
    product_names.append(product_name)
    product_prices.append(product_price)
    ratings.append(rating)
    reviews.append(review)
    
    # Merge product data into the product_data dictionary
    product_data['Product URL'] = product_url
    product_data['Product Name'] = product_name
    product_data['Product Price'] = product_price
    product_data['Rating'] = rating
    product_data['Number of Reviews'] = review
    
    # Export data to a CSV file
    pd.DataFrame([product_data]).to_csv('amazon_products20.csv', mode='a', header=False, index=False)

print('Scraping and CSV export complete.')
