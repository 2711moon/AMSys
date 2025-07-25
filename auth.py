from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from forms import LoginForm, CSRFOnlyForm
from models import users_collection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        flash('You must be logged in to change your password.', 'warning')
        return redirect(url_for('auth.login'))

    form = CSRFOnlyForm()

    if request.method == 'POST':
        current_pw = request.form.get('current_password')
        new_pw = request.form.get('new_password')
        confirm_pw = request.form.get('confirm_password')

        user = users_collection.find_one({'username': session['username']})

        if not user or not check_password_hash(user['password'], current_pw):
            flash('Current password is incorrect.', 'danger')
        elif new_pw != confirm_pw:
            flash('New passwords do not match.', 'warning')
        else:
            hashed = generate_password_hash(new_pw, method='pbkdf2:sha256')
            users_collection.update_one(
                {'_id': user['_id']},
                {'$set': {'password': hashed}}
            )
            flash('Password updated successfully.', 'success')
            return redirect(url_for('main.dashboard'))

    return render_template('auth/change_password.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        identifier = request.form['identifier']
        password = request.form['passcode']

        user = users_collection.find_one({'username': identifier})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['role'] = user.get('role', 'user')
            flash('Login successful.', 'success')
            #next_page = request.args.get('next')
            return redirect(url_for('main.dashboard'))
            
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
