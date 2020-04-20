from flask import request
from util.utils import json_response, JSON_MIME_TYPE
import ssl
from time import strftime
import traceback
from . import routes
import json
import logging
from service import storie_service


@routes.errorhandler(Exception)
def exceptions(e):
    ts = strftime('[%Y-%b-%d %H:%M:%S]')
    tb = traceback.format_exc()
    logging.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500

@routes.route('/', methods=['GET'])
def getHome():
  return "Welcome to Graphy"

@routes.route('/getAll', methods=['GET'])
def getAllStories():
  return json_response(storie_service.get_all_stories(0, is_by_user_id=False))

@routes.route('/get-by-user_id', methods=['GET'])
def get_stories_by_user_id():
  user_id = None
  if request.args:
    user_id = request.args.get('user_id')
  return json_response(storie_service.get_all_stories(user_id, is_by_user_id=True))

@routes.route('/create-story', methods=['POST'])
def create_story():
  return json_response(storie_service.create_new_story(request))
