from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

DATABASE = 'books'


class Book:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(DATABASE).query_db(query)
        books = []
        for book in results:
            books.append(Book(book))
        return books

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        book = Book(result[0])
        return book

    @classmethod
    def update(cls, data):
        query = "UPDATE books SET name = %(name)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_book_with_users(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN users ON favorites.user_id = users.id WHERE books.id = %(id)s;"
        results = connectToMySQL('books').query_db(query, data)
        # results will be a list of book objects with the user attached to each row.
        book = cls(results[0])
        for row_from_db in results:
            # Now we parse the book data to make instances of books ="keyword from-rainbow">and add them into our list.
            user_data = {
                "id": row_from_db["users.id"],
                "name": row_from_db["name"],
                "bun": row_from_db["bun"],
                "calories": row_from_db["calories"],
                "created_at": row_from_db["books.created_at"],
                "updated_at": row_from_db["books.updated_at"]
            }
            book.on_users.append(user.User(user_data))
        return book
