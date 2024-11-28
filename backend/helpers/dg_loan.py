from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_loan


def create_loan():
    response = {}
    try:
        
        # Créer une nouvelle instance de prêt
        new_loan = dg_loan()
        new_loan.l_user_u_uid = request.json.get('l_user_u_uid')
        new_loan.l_book_id = request.json.get('l_book_id')
        new_loan.l_date = request.json.get('l_date')
        new_loan.l_return_date = request.json.get('l_return_date')
        new_loan.l_returned = request.json.get('l_returned', False)
        new_loan.l_status = request.json.get('l_status', 'Pending')
        
        # Ajouter à la base de données
        db.session.add(new_loan)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'Loan created successfully'
        response['response'] = 'success'
        response['loan_id'] = new_loan.id
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'LOAN01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_loans():
    response = {}
    try:
        
        # Récupérer tous les prêts
        loans = dg_loan.query.all()
        loans_list = []
        
        # Transformer chaque prêt en dictionnaire
        for loan in loans:
            loan_data = {}
            loan_data['id'] = loan.id
            loan_data['l_user_u_uid'] = loan.l_user_u_uid
            loan_data['l_book_id'] = loan.l_book_id
            loan_data['l_date'] = loan.l_date
            loan_data['l_return_date'] = loan.l_return_date
            loan_data['l_returned'] = loan.l_returned
            loan_data['l_status'] = loan.l_status
            loans_list.append(loan_data)
            
        # Construire la réponse
        response['loans'] = loans_list
        response['response'] = 'success'
        return jsonify(response), 200
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'LOAN02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_loan_by_id():
    response = {}
    try:
        # Récupérer l'ID du prêt depuis la requête
        loan_id = request.json.get('id')

        # Chercher le prêt
        loan = dg_loan.query.filter_by(id=loan_id).first()
        if loan:
            response['loan'] = {
                'id': loan.id,
                'l_user_u_uid': loan.l_user_u_uid,
                'l_book_id': loan.l_book_id,
                'l_date': loan.l_date,
                'l_return_date': loan.l_return_date,
                'l_returned': loan.l_returned,
                'l_status': loan.l_status
            }
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le prêt n'existe pas
        response['message'] = 'Loan not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'LOAN03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_loan():
    response = {}
    try:
        # Récupérer l'ID du prêt et les données
        loan_id = request.json.get('id')
        loan = dg_loan.query.filter_by(id=loan_id).first()

        if loan:
            # Mettre à jour les champs
            loan.l_user_u_uid = request.json.get('l_user_u_uid', loan.l_user_u_uid)
            loan.l_book_id = request.json.get('l_book_id', loan.l_book_id)
            loan.l_date = request.json.get('l_date', loan.l_date)
            loan.l_return_date = request.json.get('l_return_date', loan.l_return_date)
            loan.l_returned = request.json.get('l_returned', loan.l_returned)
            loan.l_status = request.json.get('l_status', loan.l_status)

            db.session.commit()
            response['message'] = 'Loan updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le prêt n'existe pas
        response['message'] = 'Loan not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'LOAN04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def delete_loan():
    response = {}
    try:
        
        # Récupérer l'ID du prêt depuis la requête
        loan_id = request.json.get('id')

        # Supprimer le prêt
        loan = dg_loan.query.filter_by(id=loan_id).first()
        if loan:
            db.session.delete(loan)
            db.session.commit()
            response['message'] = 'Loan deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le prêt n'existe pas
        response['message'] = 'Loan not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'LOAN05'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
