from flask_app import app, render_template, request, redirect
from flask_app.models.book import Book
from flask_app.models.user import User


@app.route('/books')
def show_books():
    books = Book.get_all()
    return render_template('books.html', books=books, page_title='Books')


# @app.route('/create/book')
# def create_book():
#     return render_template('createbook.html', page_title='Create Book', users=User.get_all())


@app.route('/post/book', methods=['POST'])
def post_book():
    Book.save(request.form)
    return redirect(f"/user/{request.form['user_id']}")


@app.route('/books/<int:id>')
def show_book(id):
    book = Book.get_book_with_users({'id': id})
    return render_template('bookusers.html', book=book)
