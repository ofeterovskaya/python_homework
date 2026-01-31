from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import json
import time

# Configure Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

# Initialize Selenium with Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Function to extract books from current page
def extract_books_from_page(page_num):
    """Extract book data from search results on the current page."""
    page_results = []

    # Find all li elements with search results
    search_results = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
    print(f"Found {len(search_results)} results on page {page_num}")

    # Extract data from each result
    for i, result in enumerate(search_results, 1):
        try:
            # Find and extract the title
            title_elem = result.find_element(By.CSS_SELECTOR, "span.title-content")
            title = title_elem.text

            # Find and extract all authors
            author_elems = result.find_elements(By.CSS_SELECTOR, "a.author-link")
            authors = [author.text for author in author_elems]
            # Join multiple authors with semicolon
            author_str = "; ".join(authors) if authors else "Unknown"

            # Find the div containing format and year, then find the span within it
            format_elem = result.find_element(By.CSS_SELECTOR, "span.display-info-primary")
            format_year = format_elem.text

            # Create a dict with the extracted data
            book_data = {
                "Title": title,
                "Author": author_str,
                "Format-Year": format_year
            }

            # Append the dict to page results
            page_results.append(book_data)

        except Exception as e:
            print(f"Error processing result {i} on page {page_num}: {e}")
            continue

    return page_results

try:
    # Base URL for search
    base_url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

    # Load the first page
    print(f"Loading page 1...")
    driver.get(base_url)
    time.sleep(3)
    print("Page 1 loaded successfully\n")

    # Determine total number of pages by looking for pagination links
    max_pages = 1  # Default to 1 page
    try:
        # Look for pagination links (they typically have page numbers)
        pagination_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='page=']")
        if pagination_links:
            # Extract page numbers from links
            page_numbers = []
            for link in pagination_links:
                href = link.get_attribute("href")
                if "page=" in href:
                    try:
                        page_num = int(href.split("page=")[1].split("&")[0])
                        page_numbers.append(page_num)
                    except:
                        continue
            if page_numbers:
                max_pages = max(page_numbers)
        print(f"Total pages to scrape: {max_pages}\n")
    except Exception as e:
        print(f"Could not determine page count, scraping page 1 only. Error: {e}\n")

    # Create an empty list to store all results
    results = []

    # Loop through all pages
    for page in range(1, max_pages + 1):
        print(f"Processing page {page} of {max_pages}...")
        
        # Load the page (skip page 1 since it's already loaded)
        if page > 1:
            page_url = f"{base_url}&page={page}"
            driver.get(page_url)
            # Pause between pages to be respectful to the server
            time.sleep(3)

        # Extract books from current page
        page_results = extract_books_from_page(page)
        results.extend(page_results)

        print(f"Extracted {len(page_results)} books from page {page}")
        print(f"Total books so far: {len(results)}\n")

        # Pause before loading next page
        if page < max_pages:
            print(f"  Pausing before next page...")
            time.sleep(2)
    print(f"Successfully extracted {len(results)} books from {max_pages} page(s)\n")

    # Create a DataFrame from the list of dicts
    df = pd.DataFrame(results)

    # Print the DataFrame
    print("=" * 80)
    print("EXTRACTED BOOKS DATA")
    print("=" * 80)
    print(df.to_string(index=False))
    print("=" * 80)

    # Optional: Save to CSV file
    # Task 4: Write the DataFrame to CSV file
    df.to_csv("get_books.csv", index=False)
    print("\nData saved to 'get_books.csv'")

    # Task 4: Write the results list to JSON file
    with open("get_books.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Data saved to 'get_books.json'")

finally:
    driver.quit()
    print("\nDriver closed")
