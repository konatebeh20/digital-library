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
from helpers.dg_article import *


class ArticleApi(Resource):
    def post(self, route):
        if route == 'CreateArticle':
            return create_article()  # Créer un article

    def get(self, route):
        if route == 'GetArticles':
            return get_articles()  # Obtenir tous les articles
        if route == 'GetArticleById':
            return get_article_by_id()  # Obtenir un article par ID

    def put(self, route):
        if route == 'UpdateArticle':
            return update_article()  # Mettre à jour un article

    def delete(self, route):
        if route == 'DeleteArticle':
            return delete_article()  # Supprimer un article
