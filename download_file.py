from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

# Set file paths
input_file = "scraped_links/generated_links.txt"  # File with URLs
download_dir = os.path.join(os.getcwd(), "downloads")  # Folder for downloads
os.makedirs(download_dir, exist_ok=True)  # Create folder if it doesn’t exist

def wait_for_download():
    """Waits for the Excel file to download and renames it with a timestamp."""
    timeout = 40
    start_time = time.time()

    while time.time() - start_time < timeout:
        files = os.listdir(download_dir)
        for file in files:
            if file.endswith(".crdownload"):  # Still downloading
                print("Waiting for download...")
                time.sleep(3)
                continue
            
            if file.endswith(".xlsx"):  # Download complete
                old_path = os.path.join(download_dir, file)
                new_name = f"{int(time.time())}_{file}"  # Add timestamp
                new_path = os.path.join(download_dir, new_name)
                
                time.sleep(3)  # Small delay before renaming
                os.rename(old_path, new_path)
                
                print(f"File saved: {new_path}")
                return new_path

        time.sleep(3)

    print("Download took too long or failed.")
    return None

def download_excel_selenium(url):
    print(f"Opening: {url}")

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")

    # Set download settings
    options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0
    })

    # Start Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 20)

        print("Waiting for page to load...")
        time.sleep(3)

        print("Looking for the download button...")

        # Open download dropdown menu
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'buttons-collection') and @title='collection']")))
        time.sleep(2)
        download_button.click()
        print("Dropdown opened.")

        # Click on Excel download option
        excel_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'buttons-excel')]")))
        time.sleep(2)
        excel_button.click()
        print("Excel download started.")

        # Wait for file to download
        file_path = wait_for_download()
        
        return file_path

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

    finally:
        driver.quit()
        print("Browser closed.")

def merge_excel_files():
    """Merges all downloaded Excel files into one."""
    merged_file_path = os.path.join(download_dir, "merged_data.xlsx")
    all_files = [f for f in os.listdir(download_dir) if f.endswith(".xlsx")]
    
    if not all_files:
        print("No Excel files found for merging.")
        return None
    
    dataframes = []
    
    for file in all_files:
        file_path = os.path.join(download_dir, file)
        try:
            df = pd.read_excel(file_path, skiprows=1)  # Skip header row
            dataframes.append(df)
            print(f"Loaded: {file}")
        except Exception as e:
            print(f"Could not read {file}: {e}")

    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        merged_df.to_excel(merged_file_path, index=False)
        print(f"Merged file saved: {merged_file_path}")
        return merged_file_path
    else:
        print("No data to merge.")
        return None

# Start the process
if __name__ == "__main__":
    if os.path.exists(input_file):
        with open(input_file, "r") as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
        
        if not urls:
            print("No URLs found in the file.")
        else:
            print(f"Found {len(urls)} URLs. Starting download...")
            for url in urls:
                file_path = download_excel_selenium(url)
                if file_path:
                    print(f"Downloaded: {file_path}")

            # Merge all Excel files
            merged_file = merge_excel_files()
            if merged_file:
                print(f"Final merged file: {merged_file}")

    else:
        print(f"File not found: {input_file}")
