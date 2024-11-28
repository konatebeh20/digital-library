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
from helpers.dg_book import *


class BookApi(Resource):
    def post(self, route):
        if route == 'CreateBook':
            return create_book()  # Créer un livre

    def get(self, route):
        if route == 'GetBooks':
            return get_books()  # Obtenir tous les livres
        if route == 'GetBookById':
            return get_book_by_id()  # Obtenir un livre par ID

    def put(self, route):
        if route == 'UpdateBook':
            return update_book()  # Mettre à jour un livre

    def delete(self, route):
        if route == 'DeleteBook':
            return delete_book()  # Supprimer un livre
