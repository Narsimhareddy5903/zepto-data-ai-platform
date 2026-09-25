import requests
import csv
from bs4 import BeautifulSoup


def extract_book(book):
    """Extract book details from a product card."""

    title = book.h3.a["title"]
    price_text = book.select_one(".price_color").get_text(strip=True)
    price = float(price_text.replace("£", "").replace("Â", ""))
    availability = book.select_one(".availability").get_text(" ", strip=True)
    availability = " ".join(availability.split())

    rating_element = book.select_one(".star-rating")

    rating_map = {
    	"One": 1,
    	"Two": 2,
    	"Three": 3,
    	"Four": 4,
    	"Five": 5
    }
 
    rating = rating_map.get(
    	rating_element.get("class")[1]
    ) if rating_element else None

    book_link = book.h3.a["href"]

    # Build the product-page URL
    if book_link.startswith("catalogue/"):
        product_url = "https://books.toscrape.com/" + book_link
    else:
        product_url = "https://books.toscrape.com/catalogue/" + book_link

    product_response = requests.get(product_url, timeout=10)

    if product_response.status_code == 200:
        product_soup = BeautifulSoup(product_response.text, "html.parser")
        product_breadcrumb = product_soup.select("ul.breadcrumb li")

        if len(product_breadcrumb) >= 3:
            category = product_breadcrumb[-2].get_text(strip=True)

            if category == "Add a comment":
                category = "Nonfiction"

        else:
            category = None
    else:
        category = None

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "category": category
    }


# Starting page
url = "https://books.toscrape.com/catalogue/page-1.html"

# Store all scraped books
books = []

# CSV output file
output_file = "data_pipeline/books.csv"

# Continue until we have at least 60 books
while url and len(books) < 60:

    response = requests.get(url, timeout=10)

    print("Status:", response.status_code)
    print("URL:", url)

    if response.status_code != 200:
        print("Failed to retrieve page.")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    book_cards = soup.select("article.product_pod")

    for book in book_cards:
        extracted = extract_book(book)
        books.append(extracted)

    print("Books collected:", len(books))

    # Find the Next button
    next_link = soup.select_one("li.next a")

    if next_link:
        next_href = next_link["href"]

        if next_href.startswith("catalogue/"):
            url = "https://books.toscrape.com/" + next_href
        else:
            url = "https://books.toscrape.com/catalogue/" + next_href
    else:
        url = None


print("Final books:", len(books))

titles = [book["title"] for book in books]

print("Unique titles:", len(set(titles)))

missing_counts = {
    field: sum(1 for book in books if book[field] is None)
    for field in books[0]
}

print("Missing values:", missing_counts)

ratings = [book["rating"] for book in books]

print("Rating values:", sorted(set(ratings)))

if books:
    print("First book:", books[0])
    print("Last book:", books[-1])

# Save cleaned data to CSV
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["title", "price", "availability", "rating", "category"]

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(books)

print("CSV file saved:", output_file)