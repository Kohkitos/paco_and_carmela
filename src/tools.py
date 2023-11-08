'''
 ______   ___    ___   _     _____
|      | /   \  /   \ | |   / ___/
|      ||     ||     || |  (   \_ 
|_|  |_||  O  ||  O  || |___\__  |
  |  |  |     ||     ||     /  \ |
  |  |  |     ||     ||     \    |
  |__|   \___/  \___/ |_____|\___|                              
'''
from preloads import *

'''
 __   ____  _     ____  _      _   _     _     
( (` | |_  | |   | |_  | |\ | | | | | | | |\/| 
_)_) |_|__ |_|__ |_|__ |_| \| |_| \_\_/ |_|  |
'''

def vid_creator_mongo(url):
    '''
    TODO
    '''

    try:
        driver = webdriver.Chrome(OPTIONS)
        driver.get(url)
    except:
        print("URL couldn't be opened")
        return 1
    
    # reject cookies
    reject_yt_cookies(driver)
   
    # take data for jsons
    title = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text
    name = driver.find_element(By.XPATH, '//*[@id="text"]/a').text
    creat_id = driver.find_element(By.XPATH, '//*[@id="owner"]/ytd-video-owner-renderer/a').get_attribute('href')[24:]

    # we don't need the driver anymore
    driver.quit()

    vid_son = {'_id': url[32:46],
                'title': title,
                'url': url,
                'platform': 'YouTube',
                'recording': {'first': datetime.now(),
                               'last': datetime.now()
                            },
               'length': '',
               'creator_id': creat_id,
               'viewers': {'max': '',
                           'min': '',
                           'avg': ''
                          }
                }

    creator_son = {'_id': creat_id,
                   'name': name,
                   'last_update': datetime.now()   
                    }

    mongo_vid_creator(vid_son, creator_son)

    return 0


def reject_yt_cookies(driver):
    '''
    TODO
    '''

    try:
        driver.find_element(By.XPATH,
                        '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button/span').click() # reject cookies
    except:
        pass

    time.sleep(2)

    try:
        driver.find_element(By.XPATH,
                        '//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click() # reject second set of cookies
    except:
        pass

    
'''
 _      ___   _      __    ___   ___   ___  
| |\/| / / \ | |\ | / /`_ / / \ | | \ | |_) 
|_|  | \_\_/ |_| \| \_\_/ \_\_/ |_|_/ |_|_) 
'''

def mongo_upload(video, creator):
    '''
    TODO
    '''   
    db.video.inser_one(video)
    
    try:
        db.creator.insert_one(creator)
    except:
        db.creator.update_one(
                    {"_id": _id},
                    {"$set": {"last_update": datetime.datetime.now()}}
                    )