import os
from dotenv import load_dotenv

load_dotenv()

POLYGON_GAS_STATION = os.getenv('POLYGON_GAS_STATION')
WEB3_HTTPProvider = os.getenv('WEB3_HTTPProvider')