from logic.logger import setup_logger
from okx.exceptions import OkxAPIException
from logic import Bot


logger = setup_logger()

if __name__ == "__main__":
    try:
        Bot().run()
    
    except KeyboardInterrupt as e:
        logger.error(f"OKX API error: {e}")
    except OkxAPIException as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Bot has stopped")