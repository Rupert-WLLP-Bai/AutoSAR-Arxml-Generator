# -*- coding: utf-8 -*-
import logging


def setup_logger():
    logger = logging.getLogger("Excel2Arxml")
    logger.setLevel(logging.WARNING)  # 测试为DEBUG, 正式使用为WARNING
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s line %(lineno)d",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


logger = setup_logger()
