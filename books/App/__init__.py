#Importación de modulos 
from flask import Flask,redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # blueprint para rutass auth en nuestra app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint para rutas auth en nuestra app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        from .models import User

        db.init_app(app)
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        
        try:
            user = User.query.filter_by(email='admin@admin.com').first()
            if not user:
                User.user()
            db.create_all() 
            
        except Exception as e:
            db.create_all()
            User.user()
            return render_template('index.html')
        
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
