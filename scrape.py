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

# Find all <h2> elements
h2_elements = soup.find_all("h2")

# Create a new HTML file to store the extracted data
with open("extracted-data.html", "w", encoding="utf-8") as file:
    file.write("<html><body>\n")
    
    # Loop through each <h2> element
    for h2 in h2_elements:
        # Write the <h2> title
        file.write(f"<h2>{h2.text}</h2>\n")
        
        # Find the next <ul> elements that follow the <h2>
        ul_elements = []
        next_element = h2.find_next_sibling()
        while next_element and next_element.name != "h2":
            if next_element.name == "ul":
                ul_elements.append(next_element)
            next_element = next_element.find_next_sibling()
        
        # Write the <ul> elements and their list items
        for ul in ul_elements:
            file.write("<ul>\n")
            for li in ul.find_all("li"):
                # Extract the URL from the <li> text
                url_text = li.text.strip()
                # Create a hyperlink for the URL
                file.write(f'<li><a href="{url_text}">{url_text}</a></li>\n')
            file.write("</ul>\n")
    
    file.write("</body></html>\n")

print("Scraping completed successfully. Data saved to extracted-data.html.")
