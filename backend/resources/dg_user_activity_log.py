import json

import requests
from bs4 import BeautifulSoup
from flask import request, jsonify
from flask_restful import Resource

from sqlalchemy import func
from sqlalchemy.sql.expression import null
#from sqlalchemy.exc import SQLAlchemyError
#from sqlalchemy.orm import sessionmaker
#from sqlalchemy import create_engine
#from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from config.constant import *
from config.db import db
from helpers.dg_user_activity_log import *


class UserActivityLogApi(Resource):
    def post(self, route):
        if route == 'LogUserActivity':
            return log_user_activity()  # Enregistre une activité utilisateur

    def get(self, route):
        if route == 'GetUserActivityLogs':
            return get_user_activity_logs()  # Récupère les logs d'activité utilisateur
