#!/usr/bin/env python3
"""
Script to convert HTML presentation to PDF with all slides
"""
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image
import img2pdf

# Configuration
HTML_FILE = "/home/prajwalj/Documents/TraditionalKnowledge_20251011_181738/Traditional-Knowledge-Presentation_20251011_181738.html"
OUTPUT_PDF = "/home/prajwalj/Documents/TraditionalKnowledge_20251011_181738/Traditional-Knowledge-Presentation-Full.pdf"
TEMP_DIR = "/home/prajwalj/Documents/TraditionalKnowledge_20251011_181738/temp_slides"

# Create temp directory
os.makedirs(TEMP_DIR, exist_ok=True)

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--force-device-scale-factor=1")

print("🚀 Starting slide capture...")

# Initialize driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the HTML file
    driver.get(f"file://{HTML_FILE}")
    time.sleep(3)  # Wait for animations to load
    
    slide_images = []
    slide_number = 1
    
    print("📸 Capturing slides...")
    
    # Capture slides by pressing Right arrow key
    while True:
        # Take screenshot
        screenshot_path = os.path.join(TEMP_DIR, f"slide_{slide_number:03d}.png")
        driver.save_screenshot(screenshot_path)
        slide_images.append(screenshot_path)
        print(f"   ✅ Captured slide {slide_number}")
        
        # Try to go to next slide
        body = driver.find_element("tag name", "body")
        body.send_keys(Keys.ARROW_RIGHT)
        time.sleep(1)  # Wait for slide transition
        
        # Check if we've reached the end (compare last two screenshots)
        if slide_number > 1:
            # Simple check: if we're still on same slide, break
            current_screenshot = os.path.join(TEMP_DIR, f"temp_check.png")
            driver.save_screenshot(current_screenshot)
            
            # Compare file sizes as a simple check
            if os.path.getsize(current_screenshot) == os.path.getsize(screenshot_path):
                os.remove(current_screenshot)
                break
            os.remove(current_screenshot)
        
        slide_number += 1
        
        # Safety limit
        if slide_number > 20:
            break
    
    print(f"\n✨ Captured {len(slide_images)} slides!")
    print("📄 Creating PDF...")
    
    # Convert images to PDF
    with open(OUTPUT_PDF, "wb") as f:
        f.write(img2pdf.convert(slide_images))
    
    print(f"\n🎉 SUCCESS! PDF saved at:\n   {OUTPUT_PDF}")
    
    # Cleanup temp files
    print("\n🧹 Cleaning up temporary files...")
    for img in slide_images:
        os.remove(img)
    os.rmdir(TEMP_DIR)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    
finally:
    driver.quit()

print("\n✅ Done!")
