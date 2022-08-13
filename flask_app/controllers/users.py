from flask_app import app, render_template, request, redirect, bcrypt, session, flash
from flask_app.models.user import User


@app.route('/')
def index():
    if 'user_id' in session:
        print('User is already logged in, displaying dashboard')
        return redirect('/dashboard')
    else:
        return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    # check if email is in database
    data = {'email': request.form['log_email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email', 'email')
        return redirect('/')
    # check password against stored hash
    if not bcrypt.check_password_hash(user_in_db.password, request.form['log_password']):
        flash('Invalid Password', 'log_password')
        return redirect('/')
    # email and password are valid
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    # if user not in session, redirect to root
    if 'user_id' not in session:
        print('User is not in session')
        return redirect('/')
    return render_template('dashboard.html')


@ app.route('/users/<int:id>')
def show_user(id):
    user = User.get_user_with_books({'id': id})
    return render_template('userbooks.html', user=user)


@ app.route('/update/user', methods=['POST'])
def update_user():
    User.update(request.form)
    return redirect(f"/user/{request.form['id']}")


@ app.route('/deactivate/<int:id>')
def deactivate(id):
    # Don't delete from db. Make user inactive.
    # User.delete({'id': id})
    return redirect('/')

# @app.route("/users")
# def show_users():
#     users = User.get_all()
#     # books_per_user = []
#     # for user in users:
#     #     books_per_user.append(
#     #         User.get_user_with_books({'id': user.id}))
#     return render_template('users.html', users=users, page_title='Users')


# @ app.route('/post_user', methods=['POST'])
# def post_user():
#     User.save(request.form)
#     return redirect('/users')
