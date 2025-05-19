import requests
from bs4 import BeautifulSoup
import csv

# URL of OLX search for "car cover"
url = "https://www.olx.in/items/q-car-cover"

# Fake browser headers to avoid blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
}

# Send GET request
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Failed to fetch data. Status: {response.status_code}")
    exit()

# Parse the page
soup = BeautifulSoup(response.text, "html.parser")

# Find all items (Note: OLX may change this class name)
items = soup.find_all("li", class_="EIR5N")

# Open CSV file to write
with open("olx_car_cover_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Price", "Location", "Link"])

    for item in items:
        title_tag = item.find("span", class_="_2tW1I")
        price_tag = item.find("span", class_="_89yzn")
        location_tag = item.find("span", class_="tjgMj")
        link_tag = item.find("a", href=True)

        title = title_tag.text.strip() if title_tag else "N/A"
        price = price_tag.text.strip() if price_tag else "N/A"
        location = location_tag.text.strip() if location_tag else "N/A"
        link = "https://www.olx.in" + link_tag['href'] if link_tag else "N/A"

        writer.writerow([title, price, location, link])

print("✅ Results saved to 'olx_car_cover_results.csv'")
