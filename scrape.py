import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://nirbytes.com/post/1000-proxies-for-school-chromebook-2024"

# Fetch the page content
response = requests.get(url)
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
