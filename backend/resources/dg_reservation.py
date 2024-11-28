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
from helpers.dg_reservation import *


class ReservationApi(Resource):
    def post(self, route):
        if route == 'CreateReservation':
            return create_reservation()  # Créer une réservation
        
    def get(self, route):
        if route == 'GetReservations':
            return get_reservations()  # Obtenir toutes les réservations
        if route == 'GetReservationById':
            return get_reservation_by_id()  # Obtenir une réservation par ID
        
    def put(self, route):
        if route == 'UpdateReservation':
            return update_reservation()  # Mettre à jour une réservation
    
    def delete(self, route):
        if route == 'DeleteReservation':
            return delete_reservation()  # Supprimer une réservation
