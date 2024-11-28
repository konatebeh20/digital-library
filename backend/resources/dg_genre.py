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
from helpers.dg_genre import *


class GenreApi(Resource):
    def post(self, route):
        if route == 'CreateGenre':
            return create_genre()  # Créer un genre

    def get(self, route):
        if route == 'GetGenres':
            return get_genres()  # Obtenir tous les genres
        if route == 'GetGenreById':
            return get_genre_by_id()  # Obtenir un genre par ID

    def put(self, route):
        if route == 'UpdateGenre':
            return update_genre()  # Mettre à jour un genre

    def delete(self, route):
        if route == 'DeleteGenre':
            return delete_genre()  # Supprimer un genre
