
from okx import AccountAPI,TradeAPI, MarketAPI
from dotenv import load_dotenv
import os
import pandas as pd
import logging

logger = logging.getLogger('trading_rsi_bot')

class Okx:
    def __init__(self): 
        load_dotenv()
        self.params = dict(
            api_key=os.getenv("API_KEY"),
            secret_key=os.getenv("SECRET_KEY"),
            passphrase=os.getenv("PASSPHRASE"),
            domain=os.getenv("DOMAIN"),
            flag=os.getenv("FLAG"),
            debug=False,
        )
        self.position_id="trading with rsi bot"
        self.symbol="BTC-USDT"
        self.qty=0.0001
        
    def check_permission(self):
        
        a = AccountAPI(**self.params).get_account_balance()

    def close_prices(self):
        candle_sticks= MarketAPI(**self.params).get_candlesticks(
            instId=self.symbol, bar='1H').get("data", [])
        candle_sticks.reverse()
        return pd.Series([float(e[4]) for e in candle_sticks])
    

    def place_order(self, side):
        po = TradeAPI(**self.params).place_order(
            instId=self.symbol,
            tdMode='cash',
            side=side,
            ordType='market',
            sz=self.qty,
            clOrdId=self.position_id
        )
        order_id = None
        if po.get("code") == "0":
            order_id = po.get("data", [ ])[0].get("ordId")
        else:
            logger.error(f"Error placing order: {po.get('msg')}")
        return order_id    
        
    
