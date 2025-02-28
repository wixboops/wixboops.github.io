import requests
from bs4 import BeautifulSoup
import time

# URL of the page to scrape
url = "https://nirbytes.com/post/1000-proxies-for-school-chromebook-2024"

# Add headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Retry settings
max_retries = 3
retry_delay = 5  # seconds

# Fetch the page content with retries
for attempt in range(max_retries):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        break  # Exit the loop if the request succeeds
    except requests.exceptions.RequestException as e:
        print(f"Attempt {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit(1)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the element with id="mcetoc_1i64jd5ii7" (category title)
category_title = soup.find(id="mcetoc_1i64jd5ii7")

# Find the <ul> elements that follow the category title
ul_elements = category_title.find_next_siblings("ul")

# Create a new HTML file to store the extracted data
with open("extracted-data.html", "w", encoding="utf-8") as file:
    file.write("<html><body>\n")
    
    # Write the category title
    if category_title:
        file.write(f"<h1>{category_title.text}</h1>\n")
    
    # Write the <ul> elements and their list items
    for ul in ul_elements:
        file.write("<ul>\n")
        for li in ul.find_all("li"):
            file.write(f"<li>{li.text}</li>\n")
        file.write("</ul>\n")
    
    file.write("</body></html>\n")

print("Scraping completed successfully. Data saved to extracted-data.html.")
