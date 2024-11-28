from flask import request, jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_article



def create_article():
    response = {}
    try:
        
        article = dg_article()
        
        new_article.r_user_u_uid = request.json.get('r_user_u_uid')
        new_article.a_title = request.json.get('a_title')
        new_article.a_abstract = request.json.get('a_abstract')
        new_article.a_content = request.json.get('a_content')
        new_article.a_publication_date = request.json.get('a_publication_date', datetime.utcnow())
        new_article.a_publication_status = request.json.get('a_publication_status', 'draft')
        
        # Ajouter à la base de données
        db.session.add(new_article)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'Article created successfully'
        response['response'] = 'success'
        response['article_id'] = new_article.id
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'ARTICLE01'
        response['error_description'] = str(e.__dict__['orig'])
        
        return jsonify(response), 400
    

def get_articles():
    response = {}
    try:
        # Récupérer tous les articles
        articles = dg_article.query.all()
        articles_list = []

        # Transformer chaque article en dictionnaire
        for article in articles:
            article_data = {}
            article_data['id'] = article.id
            article_data['r_user_u_uid'] = article.r_user_u_uid
            article_data['a_title'] = article.a_title
            article_data['a_abstract'] = article.a_abstract
            article_data['a_content'] = article.a_content
            article_data['a_publication_date'] = article.a_publication_date
            article_data['a_publication_status'] = article.a_publication_status
            articles_list.append(article_data)

        # Construire la réponse
        response['articles'] = articles_list
        response['response'] = 'success'
        return jsonify(response), 200

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'ARTICLE02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_article_by_id():
    response = {}
    try:
        # Récupérer l'ID de l'article depuis la requête
        article_id = request.json.get('id')

        # Chercher l'article
        article = dg_article.query.filter_by(id=article_id).first()
        if article:
            response['article'] = {
                'id': article.id,
                'r_user_u_uid': article.r_user_u_uid,
                'a_title': article.a_title,
                'a_abstract': article.a_abstract,
                'a_content': article.a_content,
                'a_publication_date': article.a_publication_date,
                'a_publication_status': article.a_publication_status
            }
            response['response'] = 'success'
            return jsonify(response), 200

        # Si l'article n'existe pas
        response['message'] = 'Article not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'ARTICLE03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_article():
    response = {}
    try:
        # Récupérer l'ID de l'article et les données
        article_id = request.json.get('id')
        article = dg_article.query.filter_by(id=article_id).first()

        if article:
            # Mettre à jour les champs
            article.r_user_u_uid = request.json.get('r_user_u_uid', article.r_user_u_uid)
            article.a_title = request.json.get('a_title', article.a_title)
            article.a_abstract = request.json.get('a_abstract', article.a_abstract)
            article.a_content = request.json.get('a_content', article.a_content)
            article.a_publication_date = request.json.get('a_publication_date', article.a_publication_date)
            article.a_publication_status = request.json.get('a_publication_status', article.a_publication_status)

            db.session.commit()
            response['message'] = 'Article updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si l'article n'existe pas
        response['message'] = 'Article not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'ARTICLE04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def delete_article():
    response = {}
    try:
        # Récupérer l'ID de l'article depuis la requête
        article_id = request.json.get('id')

        # Supprimer l'article
        article = dg_article.query.filter_by(id=article_id).first()
        if article:
            db.session.delete(article)
            db.session.commit()
            response['message'] = 'Article deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si l'article n'existe pas
        response['message'] = 'Article not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'ARTICLE05'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

