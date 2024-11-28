from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_genre


def create_genre():
    response = {}
    try:
        
        # Créer une nouvelle genre
        new_genre = dg_genre()
        new_genre.g_name = request.json.get('g_name')
        new_genre.g_description = request.json.get('g_description')
        
        # Ajouter le genre à la base de données
        db.session.add(new_genre)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'Genre created successfully'
        response['response'] = 'success'
        response['genre_id'] = new_genre.id
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GENRE01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_genres():
    response = {}
    try:
        
        # Récupérer tous les genres
        genres = dg_genre.query.all()
        genres_list = []

        # Transformer chaque genre en dictionnaire
        for genre in genres:
            genre_data = {
                'id': genre.id,
                'g_name': genre.g_name,
                'g_description': genre.g_description,
                'created_at': genre.created_at,
                'updated_on': genre.updated_on
            }
            genres_list.append(genre_data)
            
        
        # Construire la réponse
        response['genres'] = genres_list
        response['response'] = 'success'
        return jsonify(response), 200

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GENRE02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_genre_by_id():
    response = {}
    try:
        
        # Récupérer l'ID du genre
        genre_id = request.json.get('id')

        # Chercher le genre
        genre = dg_genre.query.filter_by(id=genre_id).first()
        if genre:
            response['genre'] = {
                'id': genre.id,
                'g_name': genre.g_name,
                'g_description': genre.g_description,
                'created_at': genre.created_at,
                'updated_on': genre.updated_on
            }
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le genre n'existe pas
        response['message'] = 'Genre not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GENRE03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_genre():
    response = {}
    try:
        
        # Récupérer l'ID du genre
        genre_id = request.json.get('id')
        genre = dg_genre.query.filter_by(id=genre_id).first()

        if genre:
            # Mettre à jour les champs
            genre.g_name = request.json.get('g_name', genre.g_name)
            genre.g_description = request.json.get('g_description', genre.g_description)
            genre.updated_on = datetime.utcnow()

            db.session.commit()
            response['message'] = 'Genre updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le genre n'existe pas
        response['message'] = 'Genre not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GENRE04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def delete_genre():
    response = {}
    try:
        
        # Récupérer l'ID du genre
        genre_id = request.json.get('id')

        # Supprimer le genre
        genre = dg_genre.query.filter_by(id=genre_id).first()
        if genre:
            db.session.delete(genre)
            db.session.commit()
            response['message'] = 'Genre deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le genre n'existe pas
        response['message'] = 'Genre not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'GENRE05'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

