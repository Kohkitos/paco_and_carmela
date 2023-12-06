from fastapi import FastAPI
from collections import defaultdict
from datetime import datetime, timedelta
from pymongo import MongoClient
from passwords import STR_CONN

app = FastAPI()

db = MongoClient(STR_CONN).final_project
db_mess = db.message

@app.get('/')
def root():
	return {'Movida': 'movidita'}

@app.get('/15_{param}')
def message_15(param):
    """
    Retrieve and organize messages based on the specified sentiment, start timestamp, and end timestamp.

    The param should be structured as follows: {SENTIMENT}-{START TIMESTAMP}-{END TIMESTAMP}.
    {SENTIMENT}: A string with POS, NEG, and NEU in any combination (e.g., POSNEG, NEGPOS, POSNEGNEU...).
    {START TIMESTAMP}: From what time to start looking, in minutes (e.g., 5, 9, 0...).
    {END TIMESTAMP}: To what time to stop looking, in minutes (e.g., 5, 9, 0...).

    Example params:
        POSNEGNEU-O-1000 (return every message).
        POS-20-25 (return positive messages on day 15 from minute 20 to 25).
        NEUNEG-0-30 (return neutral and negative messages from both days from the beginning to minute 30).

    Args:
        param (str): A string specifying the data to request.

    Returns:
        json: A JSON object with the requested data in the following structure:
            {
                'message_count': int,   # Total count of messages
                'user_count': int,      # Total count of unique users
                'SENT_messages': json   # Messages grouped by sentiment
            }
    """

    # split params into parts and split sent into a list
    params = param.split('-')
    parts = split_3(params[0])

    # initialize result dictionary and users
    users = []
    result = {}
    result['count'] = 0

    date = 1700041186843002
    end_date = 1700123057937759
    for part in parts:
        messages = list(db.message.find({'sentiment_analysis': part,
                                         'timestamp': {'$gte': int(params[1]), '$lte': int(params[2])},
                                         "unix": {"$gte": date, "$lt": end_date}})
                       )
        # prepare key names
        name = f'{part}_messages'
        count_name = f'{part}_count'
        # prepare count
        count = len(messages)
        # update users
        for message in messages:
            if message['commentator_id'] in users:
                continue
            users.append(message['commentator_id'])
        # update result
        result[name] = messages
        result[count_name] = count
        result['count'] += count

    # get the user count
    result['users'] = len(users)
    return result


@app.get('/16_{param}')
def message_16(param):
    """
    Retrieve and organize messages based on the specified sentiment, start timestamp, and end timestamp.

    The param should be structured as follows: {SENTIMENT}-{START TIMESTAMP}-{END TIMESTAMP}.
    {SENTIMENT}: A string with POS, NEG, and NEU in any combination (e.g., POSNEG, NEGPOS, POSNEGNEU...).
    {START TIMESTAMP}: From what time to start looking, in minutes (e.g., 5, 9, 0...).
    {END TIMESTAMP}: To what time to stop looking, in minutes (e.g., 5, 9, 0...).

    Example params:
        POSNEGNEU-O-1000 (return every message).
        POS-20-25 (return positive messages on day 15 from minute 20 to 25).
        NEUNEG-0-30 (return neutral and negative messages from both days from the beginning to minute 30).

    Args:
        param (str): A string specifying the data to request.

    Returns:
        json: A JSON object with the requested data in the following structure:
            {
                'message_count': int,   # Total count of messages
                'user_count': int,      # Total count of unique users
                'SENT_messages': json   # Messages grouped by sentiment
            }
    """

	# split params into parts and split sent into a list
	params = param.split('-')
	parts = split_3(params[0])

	# initialize result dictionary and users
	users = []
	result = {}
	result['count'] = 0

	date = 1700123057937759
	for part in parts:
		messages = list(db.message.find({'sentiment_analysis': part,
						'timestamp': { '$gte':  int(params[1]), '$lte': int(params[2])},
						"unix": {"$gte": date}})
		)
		# prepare key names
		name = f'{part}_messages'
		count_name = f'{part}_count'
		# prepare count
		count = len(messages)
		# update users
		for message in messages:
			if message['commentator_id'] in users:
				continue
			users.append(message['commentator_id'])
		# update result
		result[name] = messages
		result[count_name] = count
		result['count'] += count

	# get the user count	
	result['users'] = len(users)
	return result

def split_3(text):
    """
    Split a text string into parts of three characters each.

    Parameters:
    text (str): The input text to be split into parts.

    Returns:
    list: A list containing parts of the input text, each consisting of three characters.
    """

    parts = [text[i:i + 3] for i in range(0, len(text), 3)]
    return parts

@app.get('/timestamps')
def get_timestamps():
    """
    Retrieve start and end timestamps for each day in a specified date range.

    Returns a dictionary containing timestamps for each day within the date range.

    Returns:
    dict: A dictionary with day-wise start and end timestamps in the format:
          {
              day_number: {
                  'start': Start timestamp of the day (None if no data),
                  'finish': End timestamp of the day (None if no data)
              },
              ...
          }
    """
	
    dates = [datetime(2023, 11, 15, 0, 0, 0), datetime(2023, 11, 16, 0, 0, 0)]
    res = {}

    for date in dates:
        next_day = date + timedelta(days=1)
        docs = db_mess.find({
            'date': {
                '$gte': date,
                '$lt': next_day
            }
        })

        ordered = sorted(docs, key=lambda x: x['timestamp'] if 'timestamp' in x else 0)
        res[date.day] = {
            'start': ordered[0]['timestamp'] if ordered else None,
            'finish': ordered[-1]['timestamp'] if ordered else None
        }

    return res

@app.get('/max_min_{param}') # param = 'start-end'
def max_min_comments(param):
    """
    Calculate the timestamp with the maximum and minimum number of comments within a specified timestamp range.

    Parameters:
    param (str): A string containing the start and end timestamps separated by a hyphen (-) in the format 'start-end'.

    Returns:
    dict: A dictionary containing information about the timestamp with the maximum number of comments
          ('max_comments') and the timestamp with the minimum number of comments ('min_comments').
          Each entry includes the timestamp and the count of comments during that time period.
    """

    params = param.split('-')
    start_timestamp, end_timestamp = params[0], params[1]
    
    comments_count = defaultdict(int)

    messages = db.message.find({
        'timestamp': {'$gte': start_timestamp, '$lte': end_timestamp}
    })

    for message in messages:
        timestamp = message['timestamp']
        comments_count[timestamp] += 1

    max_comments_timestamp = max(comments_count, key=comments_count.get)
    max_comments_count = comments_count[max_comments_timestamp]

    min_comments_timestamp = min(comments_count, key=comments_count.get)
    min_comments_count = comments_count[min_comments_timestamp]

    return {
        "max_comments": {'timestamp': max_comments_timestamp, 'count': max_comments_count},
        "min_comments": {'timestamp': min_comments_timestamp, 'count': min_comments_count}
    }
