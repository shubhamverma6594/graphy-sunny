from constant import Commons
from async.producer import Producer
import json
import os
from config import local
import importlib.util
from constant import StoryType
from base64 import b64encode
from service.compression_service import do_compress

def process_message(body):
    request = json.loads(body.decode('utf-8'))
    event_type = request['event_type']
    event_data = json.loads(request['data'])
    print(event_data)
    try:
        print("asasas", event_data['story_id'])
        if not(Commons.mysql.is_connected()):
            return
        cursor = Commons.mysql.cursor()
        sql_select_Query = "select * from stories where id = %s order by id desc"
        cursor.execute(sql_select_Query, (event_data['story_id'],))
        
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
                story_data["data"] = b64encode(row[10]).decode('UTF-8')
            response.append(story_data)
            imagebytes = do_compress(row[10], row[6])
            
            sql_select_Query = "update stories set data = %s where id = %s order by id desc"
            cursor.execute(sql_select_Query, (imagebytes, event_data['story_id']))
            Commons.mysql.commit() 

    except Error as e:
        print("Error getting data from mysql", e)
