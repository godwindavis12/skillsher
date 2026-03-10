from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Job, Application, Course
from app import db

fresher = Blueprint('fresher', __name__, url_prefix='/fresher')

@fresher.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'fresher':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
        
    jobs = Job.query.filter_by(is_active=True).all()
    my_applications = Application.query.filter_by(fresher_id=current_user.id).all()
    
    # AI Job Recommendations (Basic Keyword Matching)
    recommended_jobs = []
    if current_user.skills:
        user_skills = [s.strip().lower() for s in current_user.skills.replace(',', ' ').split() if s.strip()]
        scored_jobs = []
        for job in jobs:
            score = 0
            job_text = f"{job.title} {job.requirements} {job.description}".lower()
            for skill in user_skills:
                if skill in job_text:
                    score += 1
            if score > 0:
                scored_jobs.append((score, job))
                
        # Sort by score descending
        scored_jobs.sort(key=lambda x: x[0], reverse=True)
        recommended_jobs = [j for score, j in scored_jobs][:5]
    
    if not recommended_jobs:
        # Fallback to newest jobs
        recommended_jobs = sorted(jobs, key=lambda x: x.posted_at, reverse=True)[:5]
        
    return render_template('fresher/dashboard.html', jobs=jobs, applications=my_applications, recommended_jobs=recommended_jobs)

@fresher.route('/jobs')
@login_required
def job_board():
    if current_user.role != 'fresher':
        return redirect(url_for('main.home'))
    jobs = Job.query.filter_by(is_active=True).all()
    return render_template('fresher/jobs.html', jobs=jobs)

@fresher.route('/apply/<int:job_id>', methods=['POST'])
@login_required
def apply_job(job_id):
    if current_user.role != 'fresher':
        return redirect(url_for('main.home'))
    job = Job.query.get_or_404(job_id)
    # Check if already applied
    existing_app = Application.query.filter_by(job_id=job.id, fresher_id=current_user.id).first()
    if existing_app:
        flash('You have already applied for this job.', 'info')
    else:
        app = Application(job_id=job.id, fresher_id=current_user.id)
        db.session.add(app)
        db.session.commit()
        flash('Application submitted successfully!', 'success')
    return redirect(url_for('fresher.dashboard'))

@fresher.route('/courses')
@login_required
def course_recommendations():
    if current_user.role != 'fresher':
        return redirect(url_for('main.home'))
    courses = Course.query.all()
    return render_template('fresher/courses.html', courses=courses)

@fresher.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role != 'fresher':
        return redirect(url_for('main.home'))
        
    if request.method == 'POST':
        from werkzeug.utils import secure_filename
        import os, time
        
        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        current_user.bio = request.form.get('bio')
        current_user.skills = request.form.get('skills')
        current_user.education = request.form.get('education')
        current_user.experience = request.form.get('experience')
        current_user.resume_url = request.form.get('resume_url')
        
        profile_image = request.files.get('profile_image')
        if profile_image and profile_image.filename:
            filename = secure_filename(profile_image.filename)
            upload_dir = os.path.join(request.environ.get('wsgi.errors').stream.name.split('app')[0], 'app', 'static', 'uploads', 'profiles')
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            upload_dir = os.path.join(base_dir, 'static', 'uploads', 'profiles')
            os.makedirs(upload_dir, exist_ok=True)
            
            filename = f"{int(time.time())}_{filename}"
            file_path = os.path.join(upload_dir, filename)
            profile_image.save(file_path)
            
            current_user.profile_image = filename
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('fresher.profile'))

    return render_template('fresher/profile.html')
