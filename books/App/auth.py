from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db


auth = Blueprint('auth', __name__)
#ruta de ingreso
@auth.route('/')
def index():
    
    return render_template('index.html')

#ruta de validación de ingreso 
@auth.route('/login', methods=['POST'])
def login():
    #se obtiene el valor de el email que viene en el post 
    email = request.form.get('email')
        #se obtiene el valor de el password que viene en el post 
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    #se selección el usuario con el email que se pasa como parametro 
    user = User.query.filter_by(email=email).first()

    #se valida si no existe el usuario y si la contraseña no coincide 
    if not user or not check_password_hash(user.password, password):
        flash('No se encontro el usuario')
        return redirect(url_for('auth.index')) # if the user doesn't exist or password is wrong, reload the page
    #se crea la sesión de usuario
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))

#ruta de cerrar sesión 
@auth.route('/logout')
@login_required
def logout():
    #se destruye la sesión de usuario
    logout_user()
    return redirect(url_for('auth.index'))    

