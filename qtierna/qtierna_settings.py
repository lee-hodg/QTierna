__appname__ = "QTierna"
import sys
import os

if 'win' in sys.platform.lower():
    APP_DATA_PATH = os.path.join(os.environ["APPDATA"], __appname__)
else:
    APP_DATA_PATH = os.path.join(os.environ["HOME"],  __appname__)

if not os.path.exists(APP_DATA_PATH):
    try:
        os.makedirs(APP_DATA_PATH)
    except Exception as e:
        APP_DATA_PATH = os.getcwd()
