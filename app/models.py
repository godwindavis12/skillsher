from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Association Table for Job and required Courses
job_courses = db.Table('job_courses',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='fresher') # admin, employer, fresher
    profile_image = db.Column(db.String(20), nullable=False, default='default.jpg')
    bio = db.Column(db.Text, nullable=True)
    
    # New Profile Fields
    full_name = db.Column(db.String(100), nullable=True)
    company_name = db.Column(db.String(100), nullable=True) # For Employers
    resume_url = db.Column(db.String(200), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)

    # Relationships
    jobs = db.relationship('Job', backref='employer', lazy=True)
    applications = db.relationship('Application', backref='applicant', lazy=True)
    employer_courses = db.relationship('Course', backref='employer', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=True)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    applications = db.relationship('Application', backref='job', lazy=True, cascade="all, delete-orphan")
    courses = db.relationship('Course', secondary=job_courses, lazy='subquery',
        backref=db.backref('jobs_required', lazy=True))

    def __repr__(self):
        return f"Job('{self.title}', '{self.location}')"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='pending') # pending, accepted, rejected
    is_viewed = db.Column(db.Boolean, default=False)
    applied_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    fresher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Application(Job: '{self.job_id}', Fresher: '{self.fresher_id}', Status: '{self.status}')"

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=True, default='default_course.jpg')
    materials_url = db.Column(db.String(200), nullable=True) # For uploaded materials
    category = db.Column(db.String(50), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Course('{self.title}', '{self.category}')"
