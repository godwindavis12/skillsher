from flask import Blueprint, render_template
from app.models import Job, Course
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.posted_at.desc()).limit(10).all()
    courses = Course.query.limit(3).all()
    
    ai_recommendation = None
    if current_user.is_authenticated and current_user.role == 'fresher':
        target_role = jobs[0].title if jobs else 'software engineer'
        ai_recommendation = {
            'message': f"Based on your profile, our AI suggests you improve your skills to match the demand for '{target_role}' roles. Start with this recommended course.",
            'course': courses[0] if courses else None
        }

    return render_template('main/home.html', jobs=jobs, ai_recommendation=ai_recommendation)

@main.route("/courses")
def courses():
    all_courses = Course.query.all()
    return render_template('main/courses.html', courses=all_courses)

@main.route("/job/<int:job_id>")
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('main/job_detail.html', job=job)

@main.route("/search")
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template('main/search_results.html', query=query, jobs=[], courses=[], employers=[])
        
    search_term = f"%{query}%"

    jobs = Job.query.filter(
        Job.is_active == True,
        (Job.title.ilike(search_term)) | (Job.description.ilike(search_term)) | (Job.requirements.ilike(search_term))
    ).all()
    
    courses = Course.query.filter(
        (Course.title.ilike(search_term)) | (Course.description.ilike(search_term)) | (Course.category.ilike(search_term))
    ).all()
    
    employers = User.query.filter(
        User.role == 'employer',
        (User.company_name.ilike(search_term)) | (User.username.ilike(search_term)) | (User.bio.ilike(search_term))
    ).all()

    return render_template('main/search_results.html', query=query, jobs=jobs, courses=courses, employers=employers)

@main.route("/company/<int:employer_id>")
def company_profile(employer_id):
    employer = User.query.get_or_404(employer_id)
    if employer.role != 'employer':
        return render_template('errors/404.html'), 404
        
    jobs = Job.query.filter_by(employer_id=employer.id, is_active=True).all()
    courses = Course.query.filter_by(employer_id=employer.id).all()
    
    return render_template('main/company_profile.html', employer=employer, jobs=jobs, courses=courses)

@main.route("/candidate/<int:fresher_id>")
def candidate_profile(fresher_id):
    fresher = User.query.get_or_404(fresher_id)
    if fresher.role != 'fresher':
        return render_template('errors/404.html'), 404
        
    return render_template('main/candidate_profile.html', fresher=fresher)
