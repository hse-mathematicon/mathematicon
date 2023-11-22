from sqlite3 import IntegrityError

from flask import redirect, url_for, flash, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from .app import app
from .user import User
from ..backend.models.database import UserDBHandler
from .. import DB_PATH

login_manager = LoginManager()
login_manager.init_app(app)

db = UserDBHandler(DB_PATH)


@login_manager.user_loader
def load_user(user_id):
    return User(DB_PATH).get(user_id)


@app.route("/logout_<lang>")
@login_required
def logout(lang):
    logout_user()
    return redirect(url_for('main_page', lang=lang))


@app.route('/register_<lang>', methods=['GET', 'POST'])
def reg_page(lang):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hashed_password, salt = User.hash_password(password)
        try:
            db.add_user(username, hashed_password, salt, email)
            flash('You\'ve been successfully logged-in')
            user = User(DB_PATH).get(username)
            login_user(user, remember=True)
            return render_template('account.html', main_lan=lang, login=current_user.username, email=current_user.email)

        except IntegrityError as e:  # если такой юзер уже есть в бд
            dupl_field = str(e).split()[-1].split('.')[-1]
            flash(f'The user with this {dupl_field} already exists')
            return redirect(url_for('reg_page', lang=lang))
    return render_template('register.html', main_lan=lang)


@app.route('/login_<lang>', methods=['GET', 'POST'])
def login(lang):
    if request.method == 'POST':
        un = request.form['username']
        user = User(DB_PATH).get(un)
        if user:
            if user.validate_password(request.form['password']):
                login_user(user, remember=True)
                flash(f'You\'ve been successfully logged-in')
                return redirect(url_for('account', lang=lang))
    return render_template('login.html', main_lan=lang)


@app.route('/account_<lang>', methods=['POST', 'GET'])
def account(lang):
    if not current_user.is_authenticated:
        return redirect(url_for('login', lang=lang))
    else:
        return render_template('account.html', main_lan=lang, login=current_user.username, email=current_user.email)


@login_required
@app.route('/favourites/', methods=['POST', 'GET'])
def remove_sent():
    user_request = request.get_json()
    if user_request['method'] == 'add':
        query = ' '.join(user_request['query'].split('+'))
        query_type = '_'.join([user_request.get('query_type', 'text'), user_request.get('search_type', 'lemma')])
        db.add_favs(current_user.id, query=query, query_type=query_type, sent_id=user_request['id'])
    elif user_request['method'] == 'delete':
        db.remove_fav(current_user.id, user_request['id'])
    return "blurp"