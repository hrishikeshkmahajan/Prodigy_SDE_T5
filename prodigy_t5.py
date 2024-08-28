import requests
from bs4 import BeautifulSoup
import csv


def extract_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    # Finding all product containers
    product_containers = soup.find_all('article', class_='product_pod')

    for product in product_containers:
        # Extracting the name of the product
        name = product.h3.a['title']

        # Extracting the price
        price = product.find('p', class_='price_color').text

        # Extracting the rating
        rating = product.p['class'][1]

        products.append({
            'name': name,
            'price': price,
            'rating': rating
        })

    return products


def save_to_csv(products, filename='products.csv'):
    keys = products[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)


def main():
    url = "http://books.toscrape.com/"
    products = extract_product_info(url)
    if products:
        save_to_csv(products)
        print(f"Data saved to {len(products)} products.")
    else:
        print("No products found or failed to extract information.")


if __name__ == "__main__":
    main()
