from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_report


def create_report():
    response = {}
    try:
        
        # Créer un nouveau rapport
        new_report = dg_report()
        new_report.rp_title = request.json.get('rp_title')
        new_report.rp_description = request.json.get('rp_description')
        new_report.rp_status = request.json.get('rp_status')
        new_report.rp_type = request.json.get('rp_type')
        new_report.rp_user_u_uid = request.json.get('rp_user_u_uid')
        new_report.rp_book_id = request.json.get('rp_book_id')
        
        # Ajouter le rapport à la base de données
        db.session.add(new_report)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'Report created successfully'
        response['response'] = 'success'
        response['report_id'] = new_report.id
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REPORT01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_reports():
    response = {}
    try:
        # Récupérer tous les rapports
        reports = dg_report.query.all()
        reports_list = []

        # Transformer chaque rapport en dictionnaire
        for report in reports:
            report_data = {
                'id': report.id,
                'rp_title': report.rp_title,
                'rp_description': report.rp_description,
                'rp_status': report.rp_status,
                'rp_type': report.rp_type,
                'rp_user_u_uid': report.rp_user_u_uid,
                'rp_book_id': report.rp_book_id,
                'rp_date': report.rp_date,
                'created_at': report.created_at,
                'updated_on': report.updated_on
            }
            reports_list.append(report_data)

        # Construire la réponse
        response['reports'] = reports_list
        response['response'] = 'success'
        return jsonify(response), 200

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REPORT02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_report_by_id():
    response = {}
    try:
        # Récupérer l'ID du rapport
        report_id = request.json.get('id')

        # Chercher le rapport
        report = dg_report.query.filter_by(id=report_id).first()
        if report:
            response['report'] = {
                'id': report.id,
                'rp_title': report.rp_title,
                'rp_description': report.rp_description,
                'rp_status': report.rp_status,
                'rp_type': report.rp_type,
                'rp_user_u_uid': report.rp_user_u_uid,
                'rp_book_id': report.rp_book_id,
                'rp_date': report.rp_date,
                'created_at': report.created_at,
                'updated_on': report.updated_on
            }
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le rapport n'existe pas
        response['message'] = 'Report not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REPORT03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_report():
    response = {}
    try:
        # Récupérer l'ID du rapport et les données
        report_id = request.json.get('id')
        report = dg_report.query.filter_by(id=report_id).first()

        if report:
            # Mettre à jour les champs
            report.rp_title = request.json.get('rp_title', report.rp_title)
            report.rp_description = request.json.get('rp_description', report.rp_description)
            report.rp_status = request.json.get('rp_status', report.rp_status)
            report.rp_type = request.json.get('rp_type', report.rp_type)
            report.rp_user_u_uid = request.json.get('rp_user_u_uid', report.rp_user_u_uid)
            report.rp_book_id = request.json.get('rp_book_id', report.rp_book_id)
            report.updated_on = datetime.utcnow()

            db.session.commit()
            response['message'] = 'Report updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le rapport n'existe pas
        response['message'] = 'Report not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REPORT04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def delete_report():
    response = {}
    try:
        # Récupérer l'ID du rapport
        report_id = request.json.get('id')

        # Supprimer le rapport
        report = dg_report.query.filter_by(id=report_id).first()
        if report:
            db.session.delete(report)
            db.session.commit()
            response['message'] = 'Report deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le rapport n'existe pas
        response['message'] = 'Report not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REPORT05'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
