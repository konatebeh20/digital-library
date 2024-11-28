from flask import request,jsonify

from sqlalchemy.exc import SQLAlchemyError

from config.constant import *
from config.db import db

from helpers.mailer import *

from model.digitallibrary import dg_book



def create_book():
    response = {}
    try:
        
        # Créer une nouvelle instance de livre
        new_book = dg_book()
        
        new_book.b_title = request.json.get('b_title')
        new_book.b_author = request.json.get('b_author')
        new_book.b_genre = request.json.get('b_genre')
        new_book.b_category = request.json.get('b_category')
        new_book.b_description = request.json.get('b_description')
        new_book.b_published_date = request.json.get('b_published_date')
        new_book.b_total_copies = request.json.get('b_total_copies')
        new_book.b_available_copies = request.json.get('b_available_copies')
        
        # Ajouter à la base de données
        db.session.add(new_book)
        db.session.commit()
        
        # Construire la réponse
        response['message'] = 'Book created successfully'
        response['response'] = 'success'
        response['book_id'] = new_book.id
        return jsonify(response), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'BOOK01'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def get_books():
    response = {}
    try:
        
        # Récupérer tous les livres
        books = dg_book.query.all()
        books_list = []
        
        # Transformer chaque livre en dictionnaire
        for book in books:
            book_data = {}
            book_data['id'] = book.id
            book_data['b_title'] = book.b_title
            book_data['b_author'] = book.b_author
            book_data['b_genre'] = book.b_genre
            book_data['b_category'] = book.b_category
            book_data['b_description'] = book.b_description
            book_data['b_published_date'] = book.b_published_date
            book_data['b_total_copies'] = book.b_total_copies
            book_data['b_available_copies'] = book.b_available_copies
            books_list.append(book_data)
            
        
        # Construire la réponse
        response['books'] = books_list
        response['response'] = 'success'
        return jsonify(response), 200
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'BOOK02'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
    

def get_book_by_id():
    response = {}
    try:
        
        # Récupérer le livre par son id depuis la requête
        book_id = request.json.get('id')
                
        # Chercher le livre
        book = dg_book.query.filter_by(id=book_id).first()
        
        if book:
            response['book'] = {
                'id': book.id,
                'b_title': book.b_title,
                'b_author': book.b_author,
                'b_genre': book.b_genre,
                'b_category': book.b_category,
                'b_description': book.b_description,
                'b_published_date': book.b_published_date,
                'b_total_copies': book.b_total_copies,
                'b_available_copies': book.b_available_copies
            }
            response['response'] = 'success'
            return jsonify(response), 200
        
        # Si le livre n'existe pas
        response['message'] = 'Book not found'
        response['response'] = 'error'
        return jsonify(response), 404
    
    except SQLAlchemyError as e:
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'BOOK03'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def update_book():
    response = {}
    try:
        
        # Récupérer l'ID du livre et les données
        book_id = request.json.get('id')
        book = dg_book.query.filter_by(id=book_id).first()
        
        if book:
            
            # Mettre à jour les champs
            book.b_title = request.json.get('b_title', book.b_title)
            book.b_author = request.json.get('b_author', book.b_author)
            book.b_genre = request.json.get('b_genre', book.b_genre)
            book.b_category = request.json.get('b_category', book.b_category)
            book.b_description = request.json.get('b_description', book.b_description)
            book.b_published_date = request.json.get('b_published_date', book.b_published_date)
            book.b_total_copies = request.json.get('b_total_copies', book.b_total_copies)
            book.b_available_copies = request.json.get('b_available_copies', book.b_available_copies)

            db.session.commit()
            response['message'] = 'Book updated successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le livre n'existe pas
        response['message'] = 'Book not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'BOOK04'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400

def delete_book():
    try:
        # Récupérer l'ID du livre depuis la requête
        book_id = request.json.get('id')
        
        if book:
            db.session.delete(book)
            db.session.commit()
            response['message'] = 'Book deleted successfully'
            response['response'] = 'success'
            return jsonify(response), 200

        # Si le livre n'existe pas
        response['message'] = 'Book not found'
        response['response'] = 'error'
        return jsonify(response), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        response['response'] = 'error'
        response['error'] = 'Unavailable'
        response['error_code'] = 'BOOK05'
        response['error_description'] = str(e.__dict__['orig'])
        return jsonify(response), 400
