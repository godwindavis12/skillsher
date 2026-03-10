from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models import Job, Application, Course
from app import db

employer = Blueprint('employer', __name__, url_prefix='/employer')

@employer.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'employer':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    courses = Course.query.filter_by(employer_id=current_user.id).all()
    return render_template('employer/dashboard.html', jobs=jobs, courses=courses)

@employer.route('/course/new', methods=['GET', 'POST'])
@login_required
def new_course():
    if current_user.role != 'employer':
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        url = request.form.get('url')
        category = request.form.get('category')
        
        materials = request.files.get('materials')
        materials_filename = None
        
        if materials and materials.filename:
            filename = secure_filename(materials.filename)
            upload_dir = os.path.join(request.environ.get('wsgi.errors').stream.name.split('app')[0], 'app', 'static', 'uploads', 'courses')
            # fallback if wsgi stream hack doesn't work locally:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            upload_dir = os.path.join(base_dir, 'static', 'uploads', 'courses')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            materials.save(file_path)
            materials_filename = filename
        
        course = Course(
            title=title, 
            description=description, 
            url=url, 
            category=category, 
            materials_url=materials_filename,
            employer_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('employer.dashboard'))
        
    return render_template('employer/new_course.html')


@employer.route('/job/new', methods=['GET', 'POST'])
@login_required
def new_job():
    if current_user.role != 'employer':
        return redirect(url_for('main.home'))
        
    courses = Course.query.all()
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        requirements = request.form.get('requirements')
        location = request.form.get('location')
        salary = request.form.get('salary')
        
        job = Job(title=title, description=description, requirements=requirements,
                  location=location, salary=salary, employer_id=current_user.id)
                  
        # Handle courses
        selected_course_ids = request.form.getlist('courses')
        for course_id in selected_course_ids:
            course = Course.query.get(int(course_id))
            if course:
                job.courses.append(course)

        db.session.add(job)
        db.session.commit()
        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer.dashboard'))
    return render_template('employer/new_job.html', courses=courses)

@employer.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    if current_user.role != 'employer':
        return redirect(url_for('main.home'))
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('employer.dashboard'))
        
    courses = Course.query.all()
        
    if request.method == 'POST':
        job.title = request.form.get('title')
        job.description = request.form.get('description')
        job.requirements = request.form.get('requirements')
        job.location = request.form.get('location')
        job.salary = request.form.get('salary')
        
        # Handle courses
        selected_course_ids = request.form.getlist('courses')
        job.courses = []
        for course_id in selected_course_ids:
            course = Course.query.get(int(course_id))
            if course:
                job.courses.append(course)
        
        db.session.commit()
        flash('Job updated successfully!', 'success')
        return redirect(url_for('employer.dashboard'))
        
    return render_template('employer/edit_job.html', job=job, courses=courses)

@employer.route('/job/<int:job_id>/delete', methods=['POST'])
@login_required
def delete_job(job_id):
    if current_user.role != 'employer':
        return redirect(url_for('main.home'))
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('employer.dashboard'))
        
    db.session.delete(job)
    db.session.commit()
    flash('Job deleted successfully!', 'success')
    return redirect(url_for('employer.dashboard'))

@employer.route('/job/<int:job_id>/applications')
@login_required
def view_applications(job_id):
    if current_user.role != 'employer':
        return redirect(url_for('main.home'))
    job = Job.query.get_or_404(job_id)
    if job.employer_id != current_user.id:
        return redirect(url_for('employer.dashboard'))
        
    applications = Application.query.filter_by(job_id=job.id).all()
    # Mark as viewed when the employer opens the applications page
    for app in applications:
        if not app.is_viewed:
            app.is_viewed = True
    db.session.commit()
    
    return render_template('employer/applications.html', job=job, applications=applications)

@employer.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'employer':
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        current_user.company_name = request.form.get('company_name')
        current_user.full_name = request.form.get('full_name')
        current_user.bio = request.form.get('bio')
        current_user.email = request.form.get('email')
        
        # Profile Image Upload
        profile_image = request.files.get('profile_image')
        if profile_image and profile_image.filename:
            filename = secure_filename(profile_image.filename)
            upload_dir = os.path.join(request.environ.get('wsgi.errors').stream.name.split('app')[0], 'app', 'static', 'uploads', 'profiles')
            # Fallback
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            upload_dir = os.path.join(base_dir, 'static', 'uploads', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Simple timestamp prefix to avoid overwrites
            import time
            filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(upload_dir, filename)
            profile_image.save(file_path)
            
            current_user.profile_image = filename
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('employer.profile'))

    return render_template('employer/profile.html')
