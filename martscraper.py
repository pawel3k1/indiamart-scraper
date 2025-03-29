from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Configuration
SEARCH_QUERY = "Acetone"  # Change this to search query you want to search for
OUTPUT_FILE = "results.txt"
CHROME_DRIVER_PATH = "C:/chromedriver/chromedriver.exe"
CHROME_BINARY_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
)
service = Service(CHROME_DRIVER_PATH)
chrome_options.binary_location = CHROME_BINARY_PATH

def scrape_indiamart(query):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    url = f"https://dir.indiamart.com/search.mp?ss={query.replace(' ', '+')}"
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "p.prd_nam"))
        )
        time.sleep(random.uniform(3, 7))  # Anti bot (low chance of getting detected but just in case, still it is very fast)
        print("Page loaded successfully!")
    except:
        print("Failed to load search results.")
        driver.quit()
        return ["No results found."]

    offers = driver.find_elements(By.CSS_SELECTOR, "p.prd_nam")
    prices = driver.find_elements(By.CLASS_NAME, "prc")  # Prices

    results = []
    for i in range(min(20, len(offers))):
        try:
            title = offers[i].text.strip()
            price = prices[i].text.strip() if i < len(prices) else "Price not listed"
            link_element = offers[i].find_element(By.XPATH, "./ancestor::a")
            link = link_element.get_attribute("href") if link_element else "No link"
            results.append(f"{title}\nPrice: {price}\nLink: {link}\n")
            print(f"Scraped: {title} - {price}")
        except Exception as e:
            print(f"Error scraping an offer: {e}")

    driver.quit()
    return results if results else ["No results found."]

def save_results(results, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(results))
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    scraped_data = scrape_indiamart(SEARCH_QUERY)
    save_results(scraped_data, OUTPUT_FILE)
