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
from helpers.dg_loan import *


class LoanApi(Resource):
    def post(self, route):
        if route == 'CreateLoan':
            return create_loan()  # Créer un prêt

    def get(self, route):
        if route == 'GetLoans':
            return get_loans()  # Obtenir tous les prêts
        if route == 'GetLoanById':
            return get_loan_by_id()  # Obtenir un prêt par ID

    def put(self, route):
        if route == 'UpdateLoan':
            return update_loan()  # Mettre à jour un prêt

    def delete(self, route):
        if route == 'DeleteLoan':
            return delete_loan()  # Supprimer un prêt
