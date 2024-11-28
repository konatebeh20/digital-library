from flask import Flask

from flask_restful import Api
# Importez votre nouvelle API
from ressources.users import UsersApi
from ressources.article import ArticleApi
from ressources.books import BooksApi
from ressources.review import ReviewApi
from ressources.reservation import ReservationApi
from ressources.report import ReportApi
from ressources.loan import LoanApi
from ressources.genre import GenreApi
from ressources.user_preferences import UserPreferencesApi
from ressources.user_activity_log import UserActivityLogApi

from config.db import db


#Initialisation de Sentry pour la gestion des erreurs
#sentry_sdk.init(
#    dsn="https://e55540efdb25abee9b6509335cfb5bae@o295794.ingest.sentry.io/4506298354499584",
#    integrations=[FlaskIntegration()],
#    traces_sample_rate=1.0
#)

#Configuration de Flask
#app.secret_key = os.urandom(24)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///unalibrar.db'

# Base de données
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_DB_URL
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Mise en place du logging
handler = logging.FileHandler('logger/app.log')
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)


app = Flask(__name__)
api = Api(app)  # Instanciation de Flask-RESTful

#Création d'une API RESTful avec Flask-Restful
#ArticleApi
api.add_resource(ArticleApi, '/api/article/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(ArticleApi, '/api/article/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(BookApi, '/api/book/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(BookApi, '/api/book/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(GenreApi, '/api/genre/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(GenreApi, '/api/genre/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(LoanApi, '/api/loan/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(LoanApi, '/api/loan/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(ReportApi, '/api/report/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(ReportApi, '/api/report/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(ReservationApi, '/api/reservation/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(ReservationApi, '/api/reservation/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(ReviewApi, '/api/review/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(ReviewApi, '/api/review/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(UserActivityLogApi, '/api/user_activity_log/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(UserActivityLogApi, '/api/user_activity_log/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(UserPreferencesApi, '/api/user_preferences/<string:route>', endpoint='cat_all', methods=["GET","POST"])
api.add_resource(UserPreferencesApi, '/api/user_preferences/<string:route>', endpoint='cat_all_patch', methods=["PATCH","DELETE"])

#ArticleApi
api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='cat_all', methods=["GET", "POST"])
api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='cat_all_patch', methods=["PATCH", "DELETE"])


#Génération de QR Code pour les reçus
img = qrcode.make(data)
img.save('static/order_qr_code.png')
send_receipt(user, order_details.id, order_details)


#Gestion des routes
@app.route(BASE_URL + '/')
def hello():
    return render_template("home.html")

db.init_app(app)


# Enregistrer les blueprints
app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(books_bp, url_prefix='/api')
app.register_blueprint(reservations_bp, url_prefix='/api')
app.register_blueprint(loans_bp, url_prefix='/api')


# Enregistrement des routes

api.add_resource(BookResource, '/books')

api.add_resource(UsersApi, '/api/users/<string:route>', endpoint='users')
api.add_resource(BooksApi, '/api/books/<string:route>', endpoint='books')
api.add_resource(ReservationsApi, '/api/reservations/<string:route>', endpoint='reservations')
api.add_resource(LoansApi, '/api/loans/<string:route>', endpoint='loans')


if __name__ == '__main__':
    app.run(debug=True)
