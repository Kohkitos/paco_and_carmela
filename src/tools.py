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

def vid_creator_pipeline(url):
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

    # creating the jsons (logging.config will be useful here)
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

    # and upload it to the database
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
 ___   _   ___   ____  _     _   _      ____ 
| |_) | | | |_) | |_  | |   | | | |\ | | |_  
|_|   |_| |_|   |_|__ |_|__ |_| |_| \| |_|__ 
'''  

def comments_pipeline(url):
    '''
    TODO
    '''
    chat = ChatDownloader().get_chat(url,
                                    retry_timeout = -1, # -1 makes the downloader to retreive a message as soon as is published
                                    timeout = 120)       # 120 secs of scrapping

     for message in chat:                        
        add_message(message)
'''
 _      ___   _      __    ___   ___   ___  
| |\/| / / \ | |\ | / /`_ / / \ | | \ | |_) 
|_|  | \_\_/ |_| \| \_\_/ \_\_/ |_|_/ |_|_) 
'''

def mongo_vid_creator(video, creator):
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

def mongo_message(message):
    '''
    TODO
    '''

    mess = message['message']
    mess_id = message['message_id']
    sent = ANALYZER.predict(message).__dict__['output']
    # common
    ts = samp['timestamp']
    # author
    name = samp['author']['name']
    com_id = samp['author']['id']

    mess_son = {
                '_id': mess_id,
                'message': mess,
                'date': datetime.datetime.now(),
                'timestamp': ts,
                'commentator_id': com_id,
                'video_title': vid_title,
                'platform': platform,
                'sentiment_analysis': sent,
                'hate_speech_analysis': hate
                }

    auth_son = {
                '_id': com_id,
                'name': name,
                'platform': platform,
                'last_update': datetime.datetime.now()
                }
    
    # just in case a commentor is a recurrent user, we will update the last_update
    try:
        db.user.insert_one(auth_son)
    except:
        db.user.update_one(
                {"_id": auth_son['_id']},
                {"$set": {"last_update": datetime.datetime.now()}}
                )
    # sometimes, a message can be recorded twice, this will prevent any error
    try:
        db.message.insert_one(mess_son)
    except:
        pass