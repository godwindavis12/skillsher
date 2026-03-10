from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Job, Course
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
    users = User.query.all()
    jobs = Job.query.all()
    courses = Course.query.all()
    return render_template('admin/dashboard.html', users=users, jobs=jobs, courses=courses)
