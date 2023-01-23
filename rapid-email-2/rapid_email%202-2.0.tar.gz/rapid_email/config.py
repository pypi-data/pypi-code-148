import logging
import os
import sys

# logging
if not os.path.exists('logs'):
    os.mkdir('logs')


logging.basicConfig(
    stream=sys.stdout,
    format='%(asctime)s - %(name)s - %(levelname)s [%(filename)s:%(lineno)s - %(funcName)s ] - %(message)s',
    level=logging.DEBUG
)

