import logging

def setup_logger(name: str = "trading_rsi_bot", log_level: int = logging.DEBUG) -> logging.Logger:
    """
    Настраивает и возвращает логгер для трейдинг-бота.
    Логи пишутся только в консоль.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Консольный обработчик
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger