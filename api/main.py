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
	elements = list(db.video.find())
	return elements

@app.get("/creator")
def creator():
	elements = list(db.creator.find())
	return elements

@app.get("/users")
def users():
	elements = list(db.user.find({}, {'_id': 1, 'last_update': 1}))
	return elements

@app.get("/messages")
def messages():
	elements = list(db.message.find())
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
		raise HTTPException(status_code=400, detail='Only "positive", "negative" or "neutral" for sentiment analysis.')

	elements = list(db.message.find({'sentiment_analysis': sent}, {}))
	return elements

@app.get("/messages_by_day/{dia}")
def messages_by_day(dia: int):
	start_date = datetime.now().replace(day=dia, hour=0, minute=0, second=0, microsecond=0)
	end_date = start_date.replace(day=(dia + 1))

	elements = list(db.message.find({"date": {"$gte": start_date, "$lt": end_date}}, {}))

	return elements

# -------- REVISAR PORQUE NO FURULA POR ALGÚN MOTIVO LLORARÉ

@app.get("/messages_by_day_and_sent/{dia}/{sent}")
def messages_by_day_and_sent(dia: int, sent: str):

	start_date = datetime.now().replace(day=dia, hour=0, minute=0, second=0, microsecond=0)
	end_date = start_date.replace(day=(dia + 1))

	if sent == 'positive':
		sent = 'POS'
	elif sent == 'neutral':
		sent = 'NEU'
	elif sent == 'negative':
		sent = 'NEG'
	else:
		raise HTTPException(status_code=400, detail='Only "positive", "negative" or "neutral" for sentiment analysis.')

	elements = list(db.message.find({"date": {"$gte": start_date, "$lt": end_date}, 'sentiment_analysis': sent}, {}))
	return elements

# --- GET COUNTS ---

@app.get("/video_count")
def count_total_vids():
	elements = list(db.video.find())
	return {"Video Count": len(elements)}

@app.get("/user_count")
def count_total_users():
	elements = list(db.user.find())
	return {"User count": len(elements)}

@app.get("/message_count")
def count_total_messages():
	elements = list(db.message.find())
	return {"Video count": len(elements)}