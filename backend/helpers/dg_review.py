from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_review


def create_review():
    response = {}
    try:
        
        # Créer une nouvelle instance de revue
        new_review = dg_review()
        
        new_review.rv_user_u_uid = request.json.get('rv_user_u_uid')
        new_review.rv_book_id = request.json.get('rv_book_id')
        new_review.rv_rating = request.json.get('rv_rating')
        new_review.rv_comment = request.json.get('rv_comment')
        new_review.rv_date = request.json.get('rv_date', datetime.utcnow())
        
        # Ajouter à la base de données
        db.session.add(new_review)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'Review created successfully'
        response['response'] = 'success'
        response['review_id'] = new_review.id
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REVIEW01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_reviews():
    response = {}
    try:
        
        # Récupérer toutes les revues
        reviews = dg_review.query.all()
        reviews_list = []

        # Transformer chaque revue en dictionnaire
        # Transformer chaque revue en dictionnaire
        for review in reviews:
            rev_data = {
                'id': review.id,
                'rv_user_u_uid': review.rv_user_u_uid,
                'rv_book_id': review.rv_book_id,
                'rv_rating': review.rv_rating,
                'rv_comment': review.rv_comment,
                'rv_date': review.rv_date
            }
            reviews_list.append(rev_data)

        # Construire la réponse
        response['reviews'] = reviews_list
        response['response'] = 'success'
        return jsonify(response), 200

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REVIEW02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_review_by_id():
    response = {}
    try:
        # Récupérer l'ID de la revue
        review_id = request.json.get('id')

        # Chercher la revue
        review = dg_review.query.filter_by(id=review_id).first()
        if review:
            response['review'] = {
                'id': review.id,
                'rv_user_u_uid': review.rv_user_u_uid,
                'rv_book_id': review.rv_book_id,
                'rv_rating': review.rv_rating,
                'rv_comment': review.rv_comment,
                'rv_date': review.rv_date
            }
            response['response'] = 'success'
            return jsonify(response), 200

        # Si la revue n'existe pas
        response['message'] = 'Review not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REVIEW03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_review():
    response = {}
    try:
        # Récupérer l'ID de la revue et les données
        review_id = request.json.get('id')
        review = dg_review.query.filter_by(id=review_id).first()

        if review:
            # Mettre à jour les champs
            review.rv_user_u_uid = request.json.get('rv_user_u_uid', review.rv_user_u_uid)
            review.rv_book_id = request.json.get('rv_book_id', review.rv_book_id)
            review.rv_rating = request.json.get('rv_rating', review.rv_rating)
            review.rv_comment = request.json.get('rv_comment', review.rv_comment)
            review.rv_date = request.json.get('rv_date', review.rv_date)

            db.session.commit()
            response['message'] = 'Review updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si la revue n'existe pas
        response['message'] = 'Review not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REVIEW04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def delete_review():
    response = {}
    try:
        
        # Récupérer l'ID de la revue
        review_id = request.json.get('id')

        # Supprimer la revue
        review = dg_review.query.filter_by(id=review_id).first()
        if review:
            db.session.delete(review)
            db.session.commit()
            response['message'] = 'Review deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si la revue n'existe pas
        response['message'] = 'Review not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'REVIEW05'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
