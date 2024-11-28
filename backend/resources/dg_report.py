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
from helpers.dg_report import *


class ReportApi(Resource):
    def post(self, route):
        if route == 'CreateReport':
            return create_report()  # Créer un rapport
        
    def get(self, route):
        if route == 'GetReports':
            return get_reports()  # Obtenir tous les rapports
        if route == 'GetReportById':
            return get_report_by_id()  # Obtenir un rapport par ID
        
    def put(self, route):
        if route == 'UpdateReport':
            return update_report()  # Mettre à jour un rapport
    
    def delete(self, route):
        if route == 'DeleteReport':
            return delete_report()  # Supprimer un rapport
