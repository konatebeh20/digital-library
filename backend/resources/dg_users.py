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
from helpers.dg_users import *
#from helpers.dg_users import CreateUsers, get_all_users, get_single_user, update_user, delete_users, verify_user


class UsersApi(Resource):
    def post(self, route):
        if route == 'createUsers':
            return create_user()
        
        if route == 'readSingleUsers':
            return get_single_user()
        
        if route == 'updateUsers':
            return update_user()
        
        if route == 'verifyUser':
            return verify_user()
    
    def patch(self, route):
        if route == 'updateUsers':
            return update_user()
    
    def delete(self, route):
        if route == 'deleteUsers':
            return delete_user()  # Cette méthode pour supprimer un utilisateur
    
    def get(self, route):
        if route == 'readUsers':
            return get_all_users()  # Cette méthode pour obtenir tous les utilisateurs
        
        if route == 'readSingleUsers':
            return get_single_user()
        
