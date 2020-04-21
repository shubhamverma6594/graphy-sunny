from constant import Commons
from constant import StoryType
import json
from base64 import b64encode
from util.utils import json_response, JSON_MIME_TYPE
import datetime
import os
import importlib.util
from async import Producer

spec = importlib.util.spec_from_file_location("module.name", "./config/local.py")
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)
producer = Producer(config.image_process_request_config, config.mq_config)

def get_all_stories(user_id, is_by_user_id):
	try:
		if not(Commons.mysql.is_connected()):
			return
		cursor = Commons.mysql.cursor()
		sql_select_Query = "select * from stories order by id desc"
		if is_by_user_id:
			sql_select_Query = "select * from stories where user_id = %s order by id desc"
			cursor.execute(sql_select_Query, (user_id,))
		else:
			cursor.execute(sql_select_Query)
		records = cursor.fetchall()
		print("Total number of rows in stories is: ", cursor.rowcount)

		response = []
		for row in records:
			story_data = {}
			story_data["id"] = row[0]
			story_data["name"] = row[1]
			story_data["user_id"] = row[2]
			story_data["user_name"] = row[3]
			story_data["description"] = row[4]
			story_data["duration"] = row[5]
			story_data["story_type"] = StoryType(row[6]).name
			story_data["lat"] = row[7]
			story_data["long"] = row[8]
			if row[10]:
				story_data["data"] = 'data:image/png;base64,' + b64encode(row[10]).decode('UTF-8')
			response.append(story_data)
		
		return json.dumps(response)
	except Error as e:
		print("Error getting data from mysql", e)
	return "Something went wrong"


def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def create_new_story(request):
	print("here is " ,request.form.get('post_data'))
	print("Posted file: {}".format(request.files['file']))
	f = request.files['file']
	f.save(f.filename)
	print(f)
	data = json.loads(request.form.get('post_data'))
	print(data)
	if not all([data.get('user_id'), data.get('name'), data.get('description'), data.get('type')]):
		error = json.dumps({'error': 'Missing field/s (user_id or name or data)'})
		return json_response(error, 400)
	user_id = data.get("user_id")
	name = data.get("name")
	description = data.get("description")
	story_type = data.get("type")
	duration = data.get("duration") if data.get("duration") != None else 0

	if story_type == 1:
		create_image_story(user_id, name, description, story_type, duration, f)

	if story_type == 2:
		create_video_story(user_id, name, description, story_type, duration, f)
	
	return "Uploaded Successfully"

def create_image_story(user_id, name, description, story_type, duration, f):
	last_id = save_story(user_id, name, description, story_type, duration, f)

	exists = os.path.isfile(f.filename)
	if exists:
		os.remove(f.filename)
		print('deleted image')

	raise_compress_event(last_id, "story_image_process")

def create_video_story(user_id, name, description, story_type, duration, f):
	last_id = save_story(user_id, name, description, story_type, duration, f)
	exists = os.path.isfile(f.filename)
	if exists:
		os.remove(f.filename)
		print('deleted vide')

	raise_compress_event(last_id, "story_video_process")


def save_story(user_id, name, description, story_type, duration, f):
	cursor = Commons.mysql.cursor()
	sql_insert_blob_query = "INSERT INTO stories (name, data, user_id, user_name, created_at, type, duration, description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
	file_data = convertToBinaryData(f.filename)
	insert_blob_tuple = (name, file_data, user_id, "veer", datetime.datetime.now(), story_type, duration, description)
	result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
	Commons.mysql.commit()
	return cursor.lastrowid


def raise_compress_event(story_id, event_type):
	event_message = {}
	event_message['event_type'] = event_type
	
	data = {}
	data['story_id'] = story_id

	event_message['data'] = json.dumps(data)
	producer.publish(event_message)

