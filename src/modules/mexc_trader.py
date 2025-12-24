from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import logging
from src.config import Config

logger = logging.getLogger(__name__)

class MEXCTrader:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.driver = browser_manager.driver
        self.wait = browser_manager.wait
        
    def open_futures_page(self, symbol):
        try:
            url = f"{Config.MEXC_BASE_URL}{symbol}"
            logger.info(f"Opening testnet futures page for {symbol}")
            self.browser.navigate_to(url)
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"Failed to open futures page: {str(e)}")
            return False
    
    def set_order_type(self, order_type):
        try:
            logger.info(f"Setting order type to {order_type}")
            
            if order_type.upper() == "LONG":
                buy_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'buy-btn') or contains(text(), 'Buy/Long')]"))
                )
                buy_button.click()
            else:
                sell_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'sell-btn') or contains(text(), 'Sell/Short')]"))
                )
                sell_button.click()
            
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"Failed to set order type: {str(e)}")
            return False
    
    def set_order_amount(self, amount_usd):
        try:
            logger.info(f"Setting order amount to ${amount_usd}")
            
            amount_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Amount' or contains(@class, 'amount-input')]"))
            )
            
            amount_input.clear()
            amount_input.send_keys(str(amount_usd))
            
            time.sleep(1)
            return True
        except Exception as e:
            logger.error(f"Failed to set order amount: {str(e)}")
            return False
    
    def set_stop_loss(self, stop_loss_percent=None):
        try:
            stop_loss_percent = stop_loss_percent or Config.DEFAULT_STOP_LOSS_PERCENT
            logger.info(f"Setting stop loss at {stop_loss_percent}%")
            
            sl_checkbox = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Stop Loss')]/preceding-sibling::input[@type='checkbox'] | //label[contains(text(), 'Stop Loss')]/input"))
            )
            
            if not sl_checkbox.is_selected():
                sl_checkbox.click()
            
            time.sleep(1)
            
            sl_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Stop Loss') or contains(@class, 'sl-input')]"))
            )
            sl_input.clear()
            sl_input.send_keys(str(stop_loss_percent))
            
            return True
        except Exception as e:
            logger.error(f"Failed to set stop loss: {str(e)}")
            return False
    
    def set_take_profit(self, take_profit_percent=None):
        try:
            take_profit_percent = take_profit_percent or Config.DEFAULT_TAKE_PROFIT_PERCENT
            logger.info(f"Setting take profit at {take_profit_percent}%")
            
            tp_checkbox = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Take Profit')]/preceding-sibling::input[@type='checkbox'] | //label[contains(text(), 'Take Profit')]/input"))
            )
            
            if not tp_checkbox.is_selected():
                tp_checkbox.click()
            
            time.sleep(1)
            
            tp_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Take Profit') or contains(@class, 'tp-input')]"))
            )
            tp_input.clear()
            tp_input.send_keys(str(take_profit_percent))
            
            return True
        except Exception as e:
            logger.error(f"Failed to set take profit: {str(e)}")
            return False
    
    def execute_trade(self, symbol, order_type, amount_usd, stop_loss_percent=None, take_profit_percent=None, execute=False):
        try:
            logger.info(f"Executing trade: {symbol} {order_type} ${amount_usd}")
            
            if not self.open_futures_page(symbol):
                return False
            
            time.sleep(2)
            
            if not self.set_order_type(order_type):
                return False
            
            if not self.set_order_amount(amount_usd):
                return False
            
            if not self.set_stop_loss(stop_loss_percent):
                return False
            
            if not self.set_take_profit(take_profit_percent):
                return False
            
            if execute:
                submit_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Open') and contains(@class, 'submit-btn')]"))
                )
                submit_button.click()
                logger.info("Trade executed successfully!")
            else:
                logger.info("Trade setup complete (not executed - set execute=True to place order)")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute trade: {str(e)}")
            return False