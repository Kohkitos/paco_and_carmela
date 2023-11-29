from fastapi import FastAPI

from datetime import datetime

from pymongo import MongoClient
from passwords import STR_CONN

cursor = MongoClient(STR_CONN)
db = cursor.final_project

app = FastAPI()

@app.get("/")
def root():
    return {"Usage": "todo"}

# --- try this later ---

# param == f"{sent}-{day}-{stime}-{etime} -- for everything: "POSNEGNEU-0-0-1000"

def user(param):
	params = param.split('-')

	users = list(db.user.find())

	if param[1] == '0':
		messages = list(db.message.find({'sentiment_analysis': {'$in': params[0]},
						 'timestamp': { '$gt':  params[2], '$lt': params[3]}})
			       )
	else:
		date = datetime.now().replace(day=int(param[1], hour=0, minute=0, second=0, microsecond=0)
		messages = list(db.message.find({'sentiment_analysis': {'$in': params[0]},
						'timestamp': { '$gt':  params[2], '$lt': params[3]},
						'date': date})
	       )

	# count = 0
	# for user in users:
	# 	for message in messages:
	# 		if user.id == message.user_id:
	# 			count += 1
	# 			break
	# return {"User count": count}

	# documents_to_update = collection.find({"timestam": {"$exists": True}})
	# updates = []
	
	# for doc in documents_to_update:
	#     new_doc = doc.copy()
	#     new_doc["timestamp"] = doc["timestam"]
	#     del new_doc["timestam"]
	#     updates.append(UpdateOne({"_id": doc["_id"]}, {"$set": new_doc}))
	
	# # Ejecutar las actualizaciones en lotes
	# if updates:
	#     result = collection.bulk_write(updates)
	#     print(f"Se han actualizado {result.modified_count} documentos")
	# else:
	#     print("No se encontraron documentos para actualizar")

@app.get("/message_{param}")
def message(param):
	params = param.split('-')
	parts = split_3(params[0])

	if params[1] == '0':
		messages = list(db.message.find({'sentiment_analysis': {'$in': parts},
						 'timestamp': { '$gte':  int(params[2]), '$lte': int(params[3])}
						 })
			       )
	else:
		date = datetime.now().replace(day=int(params[1]), hour=0, minute=0, second=0, microsecond=0)
		end_date = date.replace(day = int(param[1] + 1))

		messages = list(db.message.find({'sentiment_analysis': {'$in': parts},
						'timestamp': { '$gt':  params[2], '$lt': params[3]},
						"date": {"$gte": date, "$lt": end_date}})
	       )

		
	result ={
		'message_count': len(messages),
		'messages': messages
		}
	return result

def split_3(text):
    parts = [text[i:i + 3] for i in range(0, len(text), 3)]
    return parts