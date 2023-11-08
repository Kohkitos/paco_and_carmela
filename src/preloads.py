'''
 _     _   ___   ___    __    ___   _   ____  __  
| |   | | | |_) | |_)  / /\  | |_) | | | |_  ( (` 
|_|__ |_| |_|_) |_| \ /_/--\ |_| \ |_| |_|__ _)_) 
'''

from chat_downloader import ChatDownloader
from datetime import datetime
import time

from pymongo import MongoClient
from passwords import STR_CONN

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

'''
 ___   ___   ____  _     ___    __    ___   __  
| |_) | |_) | |_  | |   / / \  / /\  | | \ ( (` 
|_|   |_| \ |_|__ |_|__ \_\_/ /_/--\ |_|_/ _)_) 
'''

# selenium options
OPTIONS=Options()

OPTIONS.add_experimental_option('excludeSwitches', ['enable-automation'])
OPTIONS.add_experimental_option('useAutomationExtension', False)
OPTIONS.headless=False
OPTIONS.add_argument('--start-maximized')
OPTIONS.add_argument('--incognito')

# mongodb
cursor = MongoClient(STR_CONN)
db = cursor.live_chats
