from flask import Blueprint, render_template, request, redirect, url_for,flash
from flask_login import login_user, login_required, current_user
from .models import Book, Books
from . import db

main = Blueprint('main', __name__)


@main.route('/home')
@login_required
def index():
    books = Book.query.all()
    return render_template('book/view_books.html', name=current_user.name, books=books)


@main.route('/registrar')
@login_required
def libros():
    return render_template('book/registrar_libro.html')


@main.route('/regisrar-libro', methods=['POST'])
@login_required
def registrarLibro():

    if request.method == 'POST':
        name = request.form.get('name')
        quality = request.form.get('quality')
        # if this returns a user, then the email already exists in database
        book = Book.query.filter_by(name=name).first()

        if book: 
            flash('El libro con nombre {} ya existe, por favor ingresa otro.'.format(name))
            return redirect(url_for('main.libros'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.

        try:
            new_book = Book(name=name, quality=quality)
            db.session.add(new_book)
            db.session.commit()
        except Exception as e:
            flash('Fallo el registro del libro')
            return render_template('blocks/views_blocks.html')
    return redirect(url_for('main.index'))

@main.route('/actualizar/<int:id>')
@login_required
def update(id):
    book = Book.query.filter_by(id=id).first()
    return render_template('book/actualizar_libro.html',book = book)

@main.route('/actualizar-libro/<int:id>', methods=['POST'])
@login_required
def updateLibro(id):

    if request.method == 'POST':
        name = request.form.get('name')
        quality = request.form.get('quality')
        # if this returns a user, then the email already exists in database
        book = Book.query.filter_by(id=id).first()
        if book: 
            try:
                book.name = name 
                book.quality = quality
                db.session.commit()
                flash('El libro con id {} fue actualizado'.format(id))
                return redirect(url_for('main.index'))
            except Exception as e:
                flash('Fallo la actualización del libro')
                return redirect(url_for('main.index'))
           
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    
@main.route("/borrar-libro/<int:id>")
def deleteLibro(id):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    flash('El libro con id {} fue eliminado'.format(id))
    return redirect(url_for('main.index'))