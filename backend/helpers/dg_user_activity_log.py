from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_user_activity_log


def log_user_activity():
    response = {}
    try:
        
        # Récupérer les données de la requête
        user_id = request.json.get('user_id')
        activity_type = request.json.get('activity_type')
        ip_address = request.json.get('ip_address')
        user_agent = request.json.get('user_agent')
        
        # Créer une nouvelle entrée d'activité utilisateur
        new_log = dg_user_activity_log()
        new_log.user_id = user_id
        new_log.activity_type = activity_type
        new_log.ip_address = ip_address
        new_log.user_agent = user_agent
        
        # Ajouter à la base de données
        db.session.add(new_log)
        db.session.commit()
        
        # Construire la réponse de succès
        response['message'] = 'User activity logged successfully'
        response['response'] = 'success'
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        # Gérer les erreurs de base de données
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'LOG01'
        response['error_description'] = str(e.__dict__['orig'])
        
        return jsonify(response), 400
    

def get_user_activity_logs():
    response = {}
    try:
        
        # Récupérer l'ID utilisateur depuis la requête
        user_id = request.json.get('user_id')
        
        # Récupérer les logs d'activité de l'utilisateur
        logs = dg_user_activity_log.query.filter_by(user_id=user_id).all()
        logs_list = []
        
        # Ajouter chaque log au résultat
        for log in logs:
            log_data = {}
            log_data['user_id'] = log.user_id
            log_data['activity_type'] = log.activity_type
            log_data['ip_address'] = log.ip_address
            log_data['user_agent'] = log.user_agent
            log_data['timestamp'] = log.timestamp
            logs_list.append(log_data)
        
        # Construire la réponse de succès
        response['logs'] = logs_list
        response['response'] = 'success'
        return jsonify(response), 200
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'LOG02'
        response['error_description'] = str(e.__dict__['orig'])
        
        return jsonify(response), 400
    