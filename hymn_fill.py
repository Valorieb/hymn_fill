from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("hymn_scraper.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to the console
    ]
)

def main():
    logging.info("Program started.")

    # # Set up the Chrome options and service
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    logging.info("Running Chrome in headless mode (no GUI)")
    service = Service(executable_path='Z:\chromedriver-win64\chromedriver.exe') 

    driver = webdriver.Chrome(service=service, options=chrome_options)
    logging.info("WebDriver initialized with the Service")

    try:
        save_hymns_to_json(driver)
        logging.info("Program completed successfully.")
    except Exception as e:
        logging.error(f"Program terminated due to an error: {e}", exc_info=True) #includes full traceback of exception

# Scrape web for hymn data
def get_hymn_info(driver=None):
    logging.info("Scraping started.")
    hymn_list =[]
    urls = ["https://www.churchofjesuschrist.org/media/music/collections/hymns?lang=eng",
            "https://www.churchofjesuschrist.org/media/music/collections/hymns-for-home-and-church?lang=eng"
            ]
    if driver is None:
        logging.warning("No driver provided, using mock data for testing.")
        return[
            "1. The Morning Breaks",
            "2. The Spirit of God"
        ]

    try:

        for url in urls:
            logging.info(f"Fetching URL: {url}")
            driver.get(url)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".innerWrapper h4"))
            )

            # Now get the h4 elements inside the .innerWrapper
            hymn_cards = driver.find_elements(By.CSS_SELECTOR, ".innerWrapper h4")
            logging.info(f"Successfully scraped {len(hymn_cards)} hymns from {url}")

            # Add hymn info to list
            for hymn in hymn_cards:

                hymn_text = hymn.text.strip()
                # print(hymn_text)
                hymn_list.append(hymn_text)
                logging.debug(f"Added hymn: {hymn_text}")
    
    except Exception as e:
         logging.error("An error occurred during scraping!", exc_info=True)
    finally:
        logging.info("Scraping finished. Closing WebDriver...")
        driver.quit()
        logging.info("WebDriver closed.")
    
    logging.info("Scraping complete. Total hymns found: %d", len(hymn_list))

    return hymn_list

def get_hymn_dict(driver=None):
    logging.info("Converting hymn to dictionary...")
    hymn_info_list = get_hymn_info(driver)
    hymn_dict = {}

    try:
        for hymn_info in hymn_info_list:
            if ". " in hymn_info:
                number, title = hymn_info.split(". ", 1)
                title = title.split("(")[0].strip()
                hymn_dict[number] = title
            else:
                logging.warning(f"Unexpected hymn format: {hymn_info}")
    except Exception as e:
        logging.warning("Error while converting hymns to dictionary!", exc_info=True)

    logging.info(f"Conversion complete. Total hymns: {len(hymn_dict)}")

    return hymn_dict

def save_hymns_to_json(driver=None):
    logging.info("Saving hymns to JSON dictionary...")
    
    hymn_dict = get_hymn_dict(driver)

    if not hymn_dict:
        logging.warning("Hymn dictionary is empty! Skipping JSON file save.")
        return

    try:
        with open("hymns.json", "w", encoding="utf-8") as f:
            json.dump(hymn_dict, f, indent=4)
        logging.info("Hymn data successfully saved to hymns.json")
    except Exception as e:
        logging.error("Error while writing to JSON!", exc_info=True)

if __name__ == "__main__":
    main()