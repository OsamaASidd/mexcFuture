from selenium import webdriver
import time

print("Testing Chrome with Profile 2...")

options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:\Users\Abdual\AppData\Local\Google\Chrome\User Data")
options.add_argument("--profile-directory=Profile 2")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("excludeSwitches", ["enable-automation"])

try:
    print("Starting Chrome...")
    driver = webdriver.Chrome(options=options)
    
    print("Chrome started successfully!")
    
    print("Navigating to MEXC testnet...")
    driver.get("https://futures.testnet.mexc.com/futures/BTC_USDT")
    
    print("Successfully opened MEXC testnet!")
    
    time.sleep(10)
    
    driver.quit()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    input("Press Enter to close...")