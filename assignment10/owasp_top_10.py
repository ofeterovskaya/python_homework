from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import time

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
results = []

try:
    # Load the OWASP Top 10 2025 page
    driver.get('https://owasp.org/Top10/2025/')
    
    # Wait for JavaScript content to render
    time.sleep(5)

    # Find all links that contain A01-A10 (Top 10 vulnerabilities)
    all_links = driver.find_elements(By.TAG_NAME, "a")

    # Extract title and href for each Top 10 vulnerability
    for link in all_links:
        href = link.get_attribute("href") or ""
        title = link.text.strip()

        # Filter for Top 10 links (they have /A0 or /A10 in href and start with A0 or A10)
        if ("/A0" in href or "/A10" in href) and (title.startswith("A0") or title.startswith("A10")):
            if title and href:  # Ensure both title and link exist
                result_dict = {"title": title, "link": href}
                if result_dict not in results:  # Avoid duplicates
                    results.append(result_dict)

except Exception as e:
    print(f"An exception occurred: {type(e).__name__}: {e}")
finally:
    driver.quit()

# Sort by title for consistent ordering
results.sort(key=lambda x: x['title'])

# Print the list to verify data
print("\nEXTRACTED TOP 10 VULNERABILITIES:")
print("=" * 100)
print(f"{'#':<3} {'Title':<60} {'Link'}")
print("=" * 100)
for i, result in enumerate(results, 1):
    title = result["title"]
    link = result["link"]
    # Truncate link if too long for display
    display_link = link if len(link) <= 35 else link[:32] + "..."
    print(f"{i:<3} {title:<60} {display_link}")
print("=" * 100)

# Write to CSV file
with open('owasp_top_10.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Link"])
    for result in results:
        writer.writerow([result["title"], result["link"]])

print("\nData saved to owasp_top_10.csv")