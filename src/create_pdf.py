#!/usr/bin/env python3
"""
Script to convert HTML presentation to PDF with all slides
"""
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
import img2pdf
import logging

# Set up logging for robust error tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
HTML_FILE = "/home/prajwalj/Documents/TraditionalKnowledge_20251011_181738/Traditional-Knowledge-Presentation_20251011_181738.html"
OUTPUT_PDF = "/home/prajwalj/Documents/TraditionalKnowledge_20251011_181738/Traditional-Knowledge-Presentation-Full.pdf"
TEMP_DIR = "/home/prajwalj/Documents/TraditionalKnowledge_20251011_181738/temp_slides"

def capture_slides():
    """Captures slides from the HTML presentation and generates a PDF."""
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--force-device-scale-factor=1")

    logging.info("Starting slide capture...")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(f"file://{HTML_FILE}")
        time.sleep(3)  # Wait for animations to load
        
        slide_images = []
        slide_number = 1
        
        logging.info("Capturing slides...")
        
        while True:
            screenshot_path = os.path.join(TEMP_DIR, f"slide_{slide_number:03d}.png")
            driver.save_screenshot(screenshot_path)
            slide_images.append(screenshot_path)
            logging.info(f"Captured slide {slide_number}")
            
            body = driver.find_element("tag name", "body")
            body.send_keys(Keys.ARROW_RIGHT)
            time.sleep(1)
            
            if slide_number > 1:
                current_screenshot = os.path.join(TEMP_DIR, f"temp_check.png")
                driver.save_screenshot(current_screenshot)
                
                if os.path.getsize(current_screenshot) == os.path.getsize(screenshot_path):
                    os.remove(current_screenshot)
                    break
                os.remove(current_screenshot)
            
            slide_number += 1
            if slide_number > 20:
                break
        
        logging.info(f"Captured {len(slide_images)} slides!")
        logging.info("Creating PDF...")
        
        with open(OUTPUT_PDF, "wb") as f:
            f.write(img2pdf.convert(slide_images))
        
        logging.info(f"SUCCESS! PDF saved at: {OUTPUT_PDF}")
        
    finally:
        logging.info("Cleaning up temporary files...")
        for img in slide_images:
            if os.path.exists(img):
                os.remove(img)
        if os.path.exists(TEMP_DIR):
            os.rmdir(TEMP_DIR)
        driver.quit()

def main():
    try:
        capture_slides()
        logging.info("Done!")
    except Exception as e:
        # Robust try-catch at the entry point (no happy paths)
        logging.critical(f"Critical error during PDF generation: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
