import logging
import sys
from colorama import init, Fore, Style
from src.modules.browser_manager import BrowserManager
from src.modules.mexc_trader import MEXCTrader
from src.config import Config

init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, mode='a'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def print_banner():
    print(Fore.CYAN + """
    ╔═══════════════════════════════════════╗
    ║      MEXC Futures Trading Bot         ║
    ║        TESTNET - Demo Trading         ║
    ╚═══════════════════════════════════════╝
    """ + Style.RESET_ALL)

def parse_trade_input(trade_input):
    try:
        parts = trade_input.strip("{}").split(",")
        
        if len(parts) != 3:
            raise ValueError("Input must have exactly 3 parts: symbol, type, amount")
        
        symbol = parts[0].strip()
        order_type = parts[1].strip()
        amount = float(parts[2].strip())
        
        return symbol, order_type, amount
    except Exception as e:
        logger.error(f"Failed to parse input: {str(e)}")
        return None, None, None

def main():
    print_banner()
    
    browser_manager = None
    
    try:
        print(Fore.YELLOW + "\n[*] Examples of valid input:")
        print("    {SOL_USDT, LONG, 10}")
        print("    {BTC_USDT, SHORT, 50}")
        print("    Type 'exit' to quit\n" + Style.RESET_ALL)
        
        print(Fore.CYAN + "[!] For best results:")
        print("    1. Run 'python start_chrome.py' FIRST (only once)")
        print("    2. Login to MEXC in the opened Chrome")
        print("    3. Then run this bot - it will attach to that Chrome")
        print("    OR: Close all Chrome windows and run this directly\n" + Style.RESET_ALL)
        
        while True:
            trade_input = input(Fore.GREEN + "Enter trade (symbol, type, amount): " + Style.RESET_ALL)
            
            if trade_input.lower() == 'exit':
                print(Fore.YELLOW + "Exiting..." + Style.RESET_ALL)
                break
            
            symbol, order_type, amount = parse_trade_input(trade_input)
            
            if not all([symbol, order_type, amount]):
                print(Fore.RED + "Invalid input format. Please use: {SYMBOL, TYPE, AMOUNT}" + Style.RESET_ALL)
                continue
            
            if order_type.upper() not in ['LONG', 'SHORT']:
                print(Fore.RED + "Order type must be LONG or SHORT" + Style.RESET_ALL)
                continue
            
            print(Fore.CYAN + f"\n[*] Processing trade: {symbol} {order_type} ${amount}" + Style.RESET_ALL)
            
            # Initialize browser if not already done
            if browser_manager is None:
                browser_manager = BrowserManager(use_profile=True)
                browser_manager.initialize_browser()
            
            trader = MEXCTrader(browser_manager)
            
            stop_loss = Config.DEFAULT_STOP_LOSS_PERCENT
            take_profit = Config.DEFAULT_TAKE_PROFIT_PERCENT
            
            print(Fore.YELLOW + f"[*] Setting Stop Loss: {stop_loss}%" + Style.RESET_ALL)
            print(Fore.YELLOW + f"[*] Setting Take Profit: {take_profit}%" + Style.RESET_ALL)
            
            confirm = input(Fore.MAGENTA + "\nExecute trade? (yes/no): " + Style.RESET_ALL).lower()
            execute_trade = confirm == 'yes'
            
            success = trader.execute_trade(
                symbol=symbol,
                order_type=order_type,
                amount_usd=amount,
                stop_loss_percent=stop_loss,
                take_profit_percent=take_profit,
                execute=execute_trade
            )
            
            if success:
                if execute_trade:
                    print(Fore.GREEN + "\n✓ Trade executed successfully!" + Style.RESET_ALL)
                else:
                    print(Fore.GREEN + "\n✓ Trade setup complete (not executed)" + Style.RESET_ALL)
            else:
                print(Fore.RED + "\n✗ Trade failed. Check logs for details." + Style.RESET_ALL)
            
            another = input(Fore.CYAN + "\nExecute another trade? (yes/no): " + Style.RESET_ALL).lower()
            if another != 'yes':
                break
                
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\nInterrupted by user" + Style.RESET_ALL)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(Fore.RED + f"\n✗ Error: {str(e)}" + Style.RESET_ALL)
    finally:
        if browser_manager:
            browser_manager.close()
        print(Fore.CYAN + "\nGoodbye!" + Style.RESET_ALL)

if __name__ == "__main__":
    main()