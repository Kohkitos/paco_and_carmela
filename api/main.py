from fastapi import FastAPI

from datetime import datetime

from pymongo import MongoClient
from passwords import STR_CONN

cursor = MongoClient(STR_CONN)
db = cursor.final_project

app = FastAPI()

@app.get("/")
def index():
    return {"Hello": "there"}

# --- GET DICTIOS ---

@app.get("/video")
def video():
	elements = []
	for e in db.video.find():
		elements.append(e)
	return elements

@app.get("/creator")
def creator():
	elements = []
	for e in db.creator.find():
		elements.append(e)
	return elements

@app.get("/users")
def users():
	elements = []
	for e in db.user.find({}, {'_id': 1, 'last_update': 1}):
		elements.append(e)
	return elements

@app.get("/messages")
def messages():
	elements = []
	for e in db.message.find():
		elements.append(e)
	return elements

@app.get("/messages/{sent}")
def messages(sent):
	if sent == 'positive':
		sent = 'POS'
	elif sent == 'neutral':
		sent = 'NEU'
	elif sent == 'negative':
		sent = 'NEG'
	else:
		return {'Error': 'Only "positive", "negative" or "neutral" for sentiment analysis.'}
	elements = []
	for e in db.message.find({'sentiment_analysis': sent}, {}):
		elements.append(e)
	return elements

@app.get("/messages_by_day/{dia}")
def messages_by_day(dia: int):
	start_date = datetime.now().replace(day=dia, hour=0, minute=0, second=0, microsecond=0)
	end_date = start_date.replace(day=(dia + 1))

	elements = []
	for e in db.message.find({"date": {"$gte": start_date, "$lt": end_date}}, {}):
		elements.append(e)
	return elements

# --- GET COUNTS ---

@app.get("/video_count")
def count_total_vids():
	i = 0
	for e in db.video.find():
		i += 1
	return {"Video Count": i}

@app.get("/user_count")
def count_total_users():
	i = 0
	for e in db.user.find():
		i += 1
	return {"User count": i}

@app.get("/message_count")
def count_total_messages():
	i = 0
	for e in db.message.find():
		i += 1
	return {"Video count": i}

