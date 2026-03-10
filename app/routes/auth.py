from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role') # fresher or employer

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get('remember') == 'on')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'employer':
                return redirect(url_for('employer.dashboard'))
            else:
                return redirect(url_for('fresher.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html')

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))
