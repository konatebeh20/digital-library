from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_reservation


def create_reservation():
    response = {}
    try:
        # Créer une nouvelle instance de réservation
        reservation = dg_reservation()
        
        new_reservation = dg_reservation()
        new_reservation.rt_user_u_uid = request.json.get('rt_user_u_uid')
        new_reservation.rt_book_id = request.json.get('rt_book_id')
        new_reservation.rt_date = request.json.get('rt_date', datetime.utcnow())
        new_reservation.rt_status = request.json.get('rt_status', 'Pending')
        new_reservation.rt_return_date = request.json.get('rt_return_date')
        new_reservation.rt_returned = request.json.get('rt_returned', False)
        new_reservation.rt_book_status = request.json.get('rt_book_status', 'reserved')
        
        # Ajouter à la base de données
        db.session.add(new_reservation)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'Reservation created successfully'
        response['response'] = 'success'
        response['reservation_id'] = new_reservation.id
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'RESERV01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_reservations():
    response = {}
    try:
        # Récupérer toutes les réservations
        reservations = dg_reservation.query.all()
        reservations_list = []

        # Transformer chaque réservation en dictionnaire
        for reservation in reservations:
            res_data = {}
            res_data['id'] = reservation.id
            res_data['rt_user_u_uid'] = reservation.rt_user_u_uid
            res_data['rt_book_id'] = reservation.rt_book_id
            res_data['rt_date'] = reservation.rt_date
            res_data['rt_status'] = reservation.rt_status
            res_data['rt_return_date'] = reservation.rt_return_date
            res_data['rt_returned'] = reservation.rt_returned
            res_data['rt_book_status'] = reservation.rt_book_status
            reservations_list.append(res_data)

        # Construire la réponse
        response['reservations'] = reservations_list
        response['response'] = 'success'
        return jsonify(response), 200

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'RESERV02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_reservation_by_id():
    response = {}
    try:
        # Récupérer l'ID de la réservation
        reservation_id = request.json.get('id')

        # Chercher la réservation
        reservation = dg_reservation.query.filter_by(id=reservation_id).first()
        if reservation:
            response['reservation'] = {
                'id': reservation.id,
                'rt_user_u_uid': reservation.rt_user_u_uid,
                'rt_book_id': reservation.rt_book_id,
                'rt_date': reservation.rt_date,
                'rt_status': reservation.rt_status,
                'rt_return_date': reservation.rt_return_date,
                'rt_returned': reservation.rt_returned,
                'rt_book_status': reservation.rt_book_status
            }
            response['response'] = 'success'
            return jsonify(response), 200

        # Si la réservation n'existe pas
        response['message'] = 'Reservation not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'RESERV03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_reservation():
    response = {}
    try:
        # Récupérer l'ID de la réservation et les données
        reservation_id = request.json.get('id')
        reservation = dg_reservation.query.filter_by(id=reservation_id).first()

        if reservation:
            # Mettre à jour les champs
            reservation.rt_user_u_uid = request.json.get('rt_user_u_uid', reservation.rt_user_u_uid)
            reservation.rt_book_id = request.json.get('rt_book_id', reservation.rt_book_id)
            reservation.rt_date = request.json.get('rt_date', reservation.rt_date)
            reservation.rt_status = request.json.get('rt_status', reservation.rt_status)
            reservation.rt_return_date = request.json.get('rt_return_date', reservation.rt_return_date)
            reservation.rt_returned = request.json.get('rt_returned', reservation.rt_returned)
            reservation.rt_book_status = request.json.get('rt_book_status', reservation.rt_book_status)

            db.session.commit()
            response['message'] = 'Reservation updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si la réservation n'existe pas
        response['message'] = 'Reservation not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'RESERV04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def delete_reservation():
    response = {}
    try:
        # Récupérer l'ID de la réservation
        reservation_id = request.json.get('id')

        # Supprimer la réservation
        reservation = dg_reservation.query.filter_by(id=reservation_id).first()
        if reservation:
            db.session.delete(reservation)
            db.session.commit()
            response['message'] = 'Reservation deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si la réservation n'existe pas
        response['message'] = 'Reservation not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'RESERV05'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
