from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
from flask_app import flash
import re


DATABASE = 'books'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        user = User(result[0])
        return user

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET name = %(name)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        # no matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_with_books(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON favorites.user_id = users.id LEFT JOIN books ON favorites.book_id = books.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        # results will be a list of user objects with the book attached to each row.
        user = cls(results[0])
        print(user)
        for row_from_db in results:
            # Now we parse the user data to make instances of users ="keyword from-rainbow">and add them into our list.
            book_data = {
                "id": row_from_db["books.id"],
                "title": row_from_db["title"],
                "num_pages": row_from_db["num_pages"],
                "created_at": row_from_db["books.created_at"],
                "updated_at": row_from_db["books.updated_at"]
            }
            user.books.append(book.Book(book_data))
        return user

    @classmethod
    # need to pass in dictionary with user_id and book_id
    def favorite_book(cls, data):
        query = "INSERT INTO favorites (user_id, book_id) VALUES (%(user_id)s, %(book_id)s);"

    @staticmethod
    def validate_user(form: dict) -> bool:
        is_valid = True
        if len(form['first_name']) < 2:
            is_valid = False
            flash('Name must be at least 2 characters', 'first_name')
        if not form['first_name'].isalpha():
            is_valid = False
            flash('Only letters are allowed', 'first_name')
        if len(form['last_name']) < 2:
            is_valid = False
            flash('Name must be at least 2 characters', 'last_name')
        if not form['last_name'].isalpha():
            is_valid = False
            flash('Only letters are allowed', 'last_name')
        if not EMAIL_REGEX.match(form['email']):
            is_valid = False
            flash('Invalid email address', 'email')
        data = {'email': form['email']}
        user_in_db = User.get_by_email(data)
        if user_in_db:
            is_valid = False
            flash('Email is already in use. Try using it to log in.', 'email')
        if form['password'] != form['password_confirmation']:
            is_valid = False
            flash('Passwords must match', 'password')
        return is_valid
