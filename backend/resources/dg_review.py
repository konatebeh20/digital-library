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
from helpers.dg_review import *


class ReviewApi(Resource):
    def post(self, route):
        if route == 'CreateReview':
            return create_review()  # Créer un avis
        
    def get(self, route):
        if route == 'GetReviews':
            return get_reviews()  # Obtenir tous les avis
        if route == 'GetReviewById':
            return get_review_by_id()  # Obtenir un avis par ID
        
    def put(self, route):
        if route == 'UpdateReview':
            return update_review()  # Mettre à jour un avis
    
    def delete(self, route):
        if route == 'DeleteReview':
            return delete_review()  # Supprimer un avis
