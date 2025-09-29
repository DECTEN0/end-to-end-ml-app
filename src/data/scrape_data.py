import csv
import time
import random
from playwright.sync_api import sync_playwright

# Base URL for Nairobi rental properties
BASE_URL = "https://www.property24.co.ke/property-to-rent-in-nairobi-p95"

def scrape_property24(start_page=1, min_delay=2, max_delay=5):
    """Scrape property listings from Property24 Nairobi rentals."""

    listings = []
    page_num = start_page

    with sync_playwright() as p:
        # Launch headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        while True:
            url = f"{BASE_URL}?Page={page_num}"
            print(f"📄 Fetching page {page_num}… {url}")
            page.goto(url, timeout=60000)

            # Scroll to load lazy content
            scroll_height = page.evaluate("() => document.body.scrollHeight")
            for y in range(0, scroll_height, 600):
                page.evaluate(f"window.scrollTo(0, {y})")
                time.sleep(0.5)
            time.sleep(2)

            # Grab all property cards
            cards = page.query_selector_all(".js_listingTile")
            print(f"   → Found {len(cards)} listings")

            if not cards:
                print("✅ No more listings found. Stopping.")
                break

            for card in cards:
                def safe_text(selector):
                    el = card.query_selector(selector)
                    return el.inner_text().strip() if el else None

                link_el = card.query_selector("a")
                url = "https://www.property24.co.ke" + link_el.get_attribute("href") if link_el else None

                listings.append({
                    "title": safe_text(".p24_propertyTitle"),
                    "price": safe_text(".p24_price"),
                    "location": safe_text(".p24.location"),
                    "address": safe_text(".p24_address"),
                    "bathrooms": safe_text(".p24_feature_Details"),
                    "floor_size": safe_text(".p24_size"),
                    "url": url
                })

            # Random wait before next page
            delay = random.uniform(min_delay, max_delay)
            print(f"⏳ Waiting {delay:.1f}s before next page…")
            time.sleep(delay)

            page_num += 1  # Go to next page

        browser.close()

    # Save results to CSV
    output_file = "data/raw/property24_listings.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "title", "price", "location", "address",
            "bathrooms", "floor_size", "url"
        ])
        writer.writeheader()
        writer.writerows(listings)

    print(f"🏁 Done! Total properties scraped: {len(listings)}")
    print(f"📂 Data saved to {output_file}")

    return listings


if __name__ == "__main__":
    scrape_property24(start_page=1)