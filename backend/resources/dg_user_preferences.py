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
from helpers.dg_user_preferences import *
#from helpers.user_preferences import create_user_preferences, get_user_preferences, update_user_preferences, delete_user_preferences


class UserPreferencesApi(Resource):
    def post(self, route):
        if route == 'CreateUserPreferences':
            # Récupérer les données à partir de la requête
            data = request.get_json()  # On suppose que les données sont envoyées en JSON
            return create_user_preferences(data)

    def get(self, route):
        if route == 'GetUserPreferences':
            return get_user_preferences()  # Renvoie les préférences d'un utilisateur

    def patch(self, route):
        if route == 'UpdateUserPreferences':
            data = request.get_json()  # Les données mises à jour sont envoyées en JSON
            return update_user_preferences(data)

    def delete(self, route):
        if route == 'DeleteUserPreferences':
            data = request.get_json()  # Suppression des préférences avec l'ID de l'utilisateur
            return delete_user_preferences(data)
        