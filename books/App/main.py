from flask import Blueprint, render_template, request, redirect, url_for,flash
from flask_login import login_user, login_required, current_user
from .models import Book
from . import db

main = Blueprint('main', __name__)


@main.route('/home')
@login_required
def index():
    books = Book.query.all()
    return render_template('book/view_books.html', name=current_user.name, books=books)

#ruta para vista de registrar libros 
@main.route('/registrar')
@login_required
def libros():
    #renderiza la plantilla pasada como parametro
    return render_template('book/registrar_libro.html')

#ruta de función final de registro 
@main.route('/regisrar-libro', methods=['POST'])
@login_required
def registrarLibro():
    #se valida si el metodo de el request es POST 
    if request.method == 'POST':
        #si es así captura los datos de los libros 
        name = request.form.get('name')
        quality = request.form.get('quality')
        #Busca en la base de datos si existe el libro 
        book = Book.query.filter_by(name=name).first()
        #si ya existe el libro lo redirecciona a la vista de registrar y le pide que ingrese otro 
        if book: 
            flash('El libro con nombre {} ya existe, por favor ingresa otro.'.format(name))
            return redirect(url_for('main.libros'))
        #registra el libro, si falla arroja el error y redirecciona a la vista de libros 
        try:
            new_book = Book(name=name, quality=quality)
            db.session.add(new_book)
            db.session.commit()
        except Exception as e:
            flash('Fallo el registro del libro')
            return render_template('blocks/views_blocks.html')
    #si no falla el registro del libro redirecciona a la vista de libros con el registro creado    
    return redirect(url_for('main.index'))

#ruta vista de formulario de actualización 
@main.route('/actualizar/<int:id>')
@login_required
def update(id):
    #recibe como parametro el id del libro  y busca el libro con ese id en la base de datos 
    book = Book.query.filter_by(id=id).first()
    return render_template('book/actualizar_libro.html',book = book)

#Ruta funcion de actualizar 
@main.route('/actualizar-libro/<int:id>', methods=['POST'])
@login_required
def updateLibro(id):
    #Se valida si el metodo del request es post
    if request.method == 'POST':
        #Se capturan los datos pasados en el formulario 
        name = request.form.get('name')
        quality = request.form.get('quality')
        #Se busca el libro con el id pasado como parametro y se actualiza 
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

#funcion de eliminar libro                
@main.route("/borrar-libro/<int:id>")
def deleteLibro(id):
    #se busca el libro en la base de datos y se elimina 
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    #redirecciona a la vista de libros con el mensaje de eliminado 
    flash('El libro con id {} fue eliminado'.format(id))
    return redirect(url_for('main.index'))