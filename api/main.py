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
	This is a function that returns a JSON serching for the values specified in the param.

	The param should be structure as follows: {SENTIMEN}-{START TIMESTAMP}-{END TIMESTAMP}.
	{SENTIMENT}: a string with POS, NEG and NEU in any combination (e.g: POSNEG, NEGPOS, POSNEGNEU...)
	{START TIMESTAMP}: from what time you want to look or in minutes (e.g: 5, 9, 0...)
	{END TIMESTAMP}: to what time you want to look or in minutes (e.g: 5, 9, 0...)

	Example of params:
		POSNEGNEU-O-1000 	(this param will return every message).
		POS-20-25			(this param will return positive messages on day 15 from minute 20 to 25)
		NEUNEG-0-30			(this param will return neutral and negative message from both days from the beggining to minute 30)

	Args:
		param (str): a string with the data to request.

	Returns:
		json: a JSON with the data requested as follows:
			{message_count: 		int,
			user_count:				int,
			SENT_messages:			json}
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
						'timestamp': { '$gte':  int(params[1]), '$lte': int(params[2])},
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
	This is a function that returns a JSON serching for the values specified in the param.

	The param should be structure as follows: {SENTIMEN}-{START TIMESTAMP}-{END TIMESTAMP}.
	{SENTIMENT}: a string with POS, NEG and NEU in any combination (e.g: POSNEG, NEGPOS, POSNEGNEU...)
	{START TIMESTAMP}: from what time you want to look or in minutes (e.g: 5, 9, 0...)
	{END TIMESTAMP}: to what time you want to look or in minutes (e.g: 5, 9, 0...)

	Example of params:
		POSNEGNEU-O-1000 	(this param will return every message).
		POS-20-25			(this param will return positive messages on day 15 from minute 20 to 25)
		NEUNEG-0-30			(this param will return neutral and negative message from both days from the beggining to minute 30)

	Args:
		param (str): a string with the data to request.

	Returns:
		json: a JSON with the data requested as follows:
			{message_count: 		int,
			user_count:				int,
			SENT_messages:			json}
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
    parts = [text[i:i + 3] for i in range(0, len(text), 3)]
    return parts

@app.get('/timestamps')
def get_timestamps():
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
