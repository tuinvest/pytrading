import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s [%(module)11s] [%(levelname)7s] %(message)s')
