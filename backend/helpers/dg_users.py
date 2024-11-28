from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_users

def create_user():
    response = {}
    try:
        
        newUser = dg_users()
        
        newUser.u_name = request.json.get('u_name')
        newUser.u_firstname = request.json.get('u_firstname')
        newUser.u_lastname = request.json.get('u_lastname')
        newUser.u_username = request.json.get('u_username')
        newUser.u_mobile = request.json.get('u_mobile')
        newUser.u_address = request.json.get('u_address')
        newUser.u_country = request.json.get('u_country')
        newUser.u_state = request.json.get('u_state')
        newUser.u_city = request.json.get('u_city')
        newUser.u_email = request.json.get('u_email')
        newUser.u_image_link = request.json.get('u_image_link')
        newUser.u_status = 1  # Statut actif par défaut
        newUser.u_password_hash = request.json.get('u_password')  # Assurez-vous que le mot de passe est haché
        newUser.u_first_login = request.json.get('u_first_login', True)
        
        db.session.add(newUser)
        db.session.commit()
        
        response['u_uid'] = newUser.u_uid
        response['u_firstname'] = newUser.u_firstname
        response['u_lastname'] = newUser.u_lastname
        response['response'] = 'success'
        
        return jsonify(response), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
    
    except Exception as e:
        # En cas d'autres erreurs, renvoyer une réponse générique
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU02'
        response['error_description'] = str(e)
        return jsonify(response), 500
    

def get_all_users():
    response = {}
    try:
        
        users = dg_users.query.all()
        users_list = [user.as_dict() for user in users]
        
        response['users'] = users_list
        response['response'] = 'success'
        
        return jsonify({"users": users_list}), 200
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU01'
        response['error_description'] = str(e.__dict__['orig'])
        
        return jsonify(response), 400

def get_user_by_id(u_uid):
    response = {}
    try:
        
        user = dg_users.query.filter_by(u_uid=u_uid).first()
        
        if user:
            response['result'] = user.as_dict()
            response['response'] = 'success'
            return jsonify(response), 200
        else:
            response['response'] = 'error'
            response['message'] = 'User not found'
            return jsonify(response), 404
        
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU03'
        response['error_description'] = str(e.__dict__['orig'])
        
        return jsonify(response), 400
    

def update_user(u_uid):
    response = {}
    try:
        
        user = dg_users.query.filter_by(u_uid=u_uid).first()
        
        if user:
            response['result'] = user.as_dict()
            response['response'] = 'success'
            return jsonify(response), 200
        else:
            response['response'] = 'error'
            response['message'] = 'User not found'
            return jsonify(response), 404
        
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU03'
        response['error_description'] = str(e.__dict__['orig'])
        
        return jsonify(response), 400
    

def delete_user(u_uid):
    response = {}
    try:
        
        user = dg_users.query.filter_by(u_uid=u_uid).first()
        if user:
            data = request.json
            
            for key, value in data.items():
                setattr(user, key, value)
                
            # db.session.delete(user)
            db.session.commit()
            
            response['message'] = 'User updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200
        else:
            response['message'] = 'User not found'
            response['response'] = 'error'
            return jsonify(response), 404
        
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GOU02'
        response['error_description'] = str(e.__dict__['orig'])
        
        return jsonify(response), 400
    