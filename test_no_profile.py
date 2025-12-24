from selenium import webdriver
import time

print("Testing Chrome WITHOUT profile...")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

try:
    print("Starting Chrome...")
    driver = webdriver.Chrome(options=options)
    
    print("Chrome started successfully!")
    
    print("Navigating to MEXC testnet...")
    driver.get("https://futures.testnet.mexc.com/futures/BTC_USDT")
    
    print("Successfully opened MEXC testnet!")
    print("Browser will stay open for 30 seconds...")
    
    time.sleep(30)
    
    driver.quit()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")