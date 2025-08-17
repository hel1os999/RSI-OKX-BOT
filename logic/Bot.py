import pandas as pd
# Imports the pandas library, which is used for data manipulation and analysis, particularly for handling time series data like price data in this case.

from logic import Okx


import logging
# Imports the logging module, which is used to log information, warnings, and errors during the bot's operation for debugging and monitoring.

from okx import AccountAPI
# Imports the AccountAPI class from the okx library, which is used to interact with the OKX exchange's account-related endpoints (e.g., fetching account balance).

from time import sleep

logger = logging.getLogger('trading_rsi_bot')

class Bot(Okx):
    def __init__(self):
        
        super(Bot, self).__init__()
        # Calls the constructor of the parent Okx class to initialize any inherited attributes or setup (e.g., API credentials, connection to OKX).

        self.timeout = 60

        self.period = 14
        # Sets the period attribute to 14, which is used as the window size for calculating the Relative Strength Index.

    def is_rsi(self):
        # Defines a method to calculate the Relative Strength Index (RSI) based on price data.

        prices = self.close_prices()

        delta = prices.diff()

        gain = delta.clip(lower=0)
        # Creates a Series where positive price changes (gains) are kept, and negative changes are set to 0 using clip.

        loss = -delta.clip(upper=0)
        # Creates a Series where negative price changes (losses) are made positive, and positive changes are set to 0.

        avg_gain = gain.rolling(window=self.period, min_periods=self.period).mean()
        # Calculates the rolling average of gains over the specified period (14 periods), requiring at least 14 data points.

        avg_loss = loss.rolling(window=self.period, min_periods=self.period).mean()
        # Calculates the rolling average of losses over the specified period (14 periods), requiring at least 14 data points.

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi

    def rsi_check(self):
        # Defines a method to check the RSI and execute trading logic based on RSI thresholds.

        rsi = self.is_rsi().iloc[-1]
        # Gets the most recent RSI value from the "is_rsi" method by selecting the last element of the RSI Series.

        try:
            #Placing an order will depend on the balance.
            balances = AccountAPI(**self.params).get_account_balance().get("data", [])
           
            usdt = float([b for b in balances[0]["details"] if b["ccy"] == "USDT"][0]["availBal"])
            
            btc = float([b for b in balances[0]["details"] if b["ccy"] == "BTC"][0]["availBal"])

            if rsi < 30 and usdt > 10:
                # Checks if the RSI is below 30 (indicating an oversold condition) and if there is more than 10 USDT available.

                order_id = self.place_order("buy")
                # If the condition is met, places a buy order for BTC by calling the `place_order` method (inherited from `Okx`) with the argument "buy".

                if order_id:
                    
                    logger.info(f"Buy order placed: {order_id}")
                   

            elif rsi > 70 and btc > 0.0001:
                # Checks if the RSI is above 70 (indicating an overbought condition) and if there is more than 0.0001 BTC available.

                order_id = self.place_order("sell")
                # If the condition is met, places a sell order for BTC by calling the place_order method with the argument "sell".

                if order_id:

                    logger.info(f"Sell order placed: {order_id}")
                    

        except Exception as e:

            logger.error(f"Error in rsi_check: {e}")
        
    def loop(self):

        while True:
            # Starts an infinite loop to keep the bot running indefinitely.

            self.rsi_check()
            

            sleep(self.timeout)
            # Pauses execution for the duration specified by self.timeout (60 seconds) before the next iteration.

    def run(self):
        # Defines a method to start the bot's operation.

        logger.info("Bot is started")
        

        try:
           

            self.check_permission()
            # Calls the `check_permission` method (inherited from `Okx`) to verify permissions before starting the bot.

            self.loop()

        except Exception as e:
            
            logger.error(f"Error in Bot run: {e}")
            