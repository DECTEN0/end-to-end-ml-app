import requests
from bs4 import BeautifulSoup
import time
import csv
import os


# Base URL for Nairobi property rentals
BASE_URL = "https://www.property24.co.ke/property-to-rent-in-nairobi-p95"

# Headers to mimic a browser (helps avoid blocking)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

# Save scraped data inside data/raw/
CSV_FILE = os.path.join("data", "raw", "property24_listings.csv")

# File to keep track of last scraped page (for resume feature)
CHECKPOINT_FILE = os.path.join("data", "raw", "last_page.txt")


def fetch_page(page):
    """Fetch the HTML content of a given page number."""
    params = {
        "propertytypes": "houses,apartments-flats,townhouses",
        "Page": page
    }
    r = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=10)
    r.raise_for_status()  # Raise error if request fails
    return r.text


def parse_listing_detail(url):
    """Extract extra info from a property detail page (description + agent)."""
    try:
        # Send request to detail page
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Extract property description
        description = soup.select_one("div.js_readMoreText")
        description_text = description.get_text(strip=True) if description else None

        # Extract agent name (if present)
        agent_name = None
        agent_tag = soup.select_one("div.agent-details h2, div.agent-details span")
        if agent_tag:
            agent_name = agent_tag.get_text(strip=True)

        return {
            "description": description_text,
            "agent_name": agent_name
        }
    except Exception as e:
        print(f"Failed to fetch detail page {url}: {e}")
        return {}


def parse_page(html):
    """Parse all property listings from one page of HTML."""
    soup = BeautifulSoup(html, "html.parser")
    listings = []

    # Each property card is inside a div with class 'p24_content'
    for card in soup.select("div.p24_content"):
        item = {}

        # Price
        price_tag = card.select_one("span.p24_price")
        item["price"] = price_tag.get_text(strip=True) if price_tag else None

        # Title (property type + area)
        title_tag = card.select_one("span.p24_title")
        item["title"] = title_tag.get_text(strip=True) if title_tag else None

        # Address
        address_tag = card.select_one("span.p24_address")
        item["address"] = address_tag.get_text(strip=True) if address_tag else None

        # Features (bedrooms, bathrooms, parking)
        features = card.select("span.p24_featureDetails")
        for f in features:
            txt = f.get_text(strip=True)
            if "Bed" in txt:
                item["bedrooms"] = txt
            elif "Bath" in txt:
                item["bathrooms"] = txt
            elif "Parking" in txt or "Garage" in txt:
                item["parking"] = txt

        # Property detail page link
        link = card.find_parent("a", href=True)
        if link:
            item["url"] = "https://www.property24.co.ke" + link["href"]

            # Fetch extra info from detail page
            detail_data = parse_listing_detail(item["url"])
            item.update(detail_data)

        listings.append(item)

    return listings


def save_csv(listings, mode="a"):
    """Save listings to CSV file (append mode by default)."""
    # Collect all keys to ensure consistent columns
    keys = set().union(*(d.keys() for d in listings))

    # Check if file already exists
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode, newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sorted(keys))

        # Write header only if creating new file
        if not file_exists or mode == "w":
            writer.writeheader()

        # Write rows
        writer.writerows(listings)


def save_checkpoint(page):
    """Save the last successfully scraped page number to file."""
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(str(page))


def load_checkpoint():
    """Load the last scraped page number, or return 1 if none found."""
    if os.path.isfile(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return int(f.read().strip())
    return 1


def scrape_all(delay=2):
    """Scrape all property pages until no more listings remain."""
    all_count = 0

    # Start from last checkpoint (or page 1 if fresh run)
    page = load_checkpoint()

    while True:
        print(f"Fetching page {page}…")
        html = fetch_page(page)
        listings = parse_page(html)

        # Stop if no listings found (end of results)
        if not listings:
            print("No more listings found. Scraping complete.")
            break

        # Show progress
        print(f"  Found {len(listings)} listings on page {page}")

        # Save results to CSV
        save_csv(listings, mode="a")
        all_count += len(listings)

        # Save checkpoint
        save_checkpoint(page)

        # Sleep to avoid getting blocked
        time.sleep(delay)

        # Next page
        page += 1

    return all_count


if __name__ == "__main__":
    print("Starting Property24 scraper…")

    # If running fresh, delete old CSV so we don't append duplicates
    if not os.path.isfile(CHECKPOINT_FILE):
        if os.path.isfile(CSV_FILE):
            os.remove(CSV_FILE)

    # Scrape all pages
    total = scrape_all(delay=2)
    print(f"Total properties scraped: {total}")
    print(f"Data saved to {CSV_FILE}")