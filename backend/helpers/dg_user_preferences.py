from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_user_preferences


def create_user_preferences():
    response = {}
    try:
        
        # Créer une nouvelle instance de préférences utilisateur
        new_preferences = dg_user_preferences()
        
        new_preferences.user_id = request.json.get('user_id')
        new_preferences.preferred_genres = request.json.get('preferred_genres')
        new_preferences.notification_settings = request.json.get('notification_settings')
        new_preferences.language_preference = request.json.get('language_preference')
        new_preferences.theme_preference = request.json.get('theme_preference')
        
        # Ajouter à la base de données
        db.session.add(new_preferences)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'User preferences created successfully'
        response['response'] = 'success'
        return jsonify(response), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'UP01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
    

def get_user_preferences():
    respons = {}
    try:
        
        user_id = request.json.get('user_id')
        
        preferences = dg_user_preferences.query.filter_by(user_id=user_id).first()

        if preferences:
            response['preferences'] = preferences.as_dict()
            response['response'] = 'success'
            return jsonify(response), 200
        
        response['message'] = 'Preferences not found'
        response['response'] = 'error'
        return jsonify(response), 404
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'UP02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_user_preferences():
    response = {}
    try:
        
        # Récupérer l'ID de l'utilisateur et les nouvelles données des préférences
        user_id = request.json.get('user_id')
        preferred_genres = request.json.get('preferred_genres')
        notification_settings = request.json.get('notification_settings')
        language_preference = request.json.get('language_preference')
        theme_preference = request.json.get('theme_preference')
        
        # Chercher les préférences de l'utilisateur
        preferences = dg_user_preferences.query.filter_by(user_id=user_id).first()
        
        if preferences:
            # Mettre à jour les champs des préférences
            preferences.preferred_genres = preferred_genres
            preferences.notification_settings = notification_settings
            preferences.language_preference = language_preference
            preferences.theme_preference = theme_preference
            
            # Sauvegarder les modifications dans la base de données
            db.session.commit()
            
            response['message'] = 'User preferences updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200
        
        # Si les préférences n'existent pas
        response['message'] = 'Preferences not found'
        response['response'] = 'error'
        return jsonify(response), 404
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'UP03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
    

def delete_user_preferences():
    response = {}
    try:
        # Récupérer l'ID de l'utilisateur
        user_id = request.json.get('user_id')

        # Chercher les préférences de l'utilisateur
        preferences = dg_user_preferences.query.filter_by(user_id=user_id).first()

        if preferences:
            # Supprimer les préférences de l'utilisateur
            db.session.delete(preferences)
            db.session.commit()
            response['message'] = 'User preferences deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si les préférences n'existent pas
        response['message'] = 'Preferences not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'UP04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
