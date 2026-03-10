from app import create_app, db, bcrypt
from app.models import User, Job, Course

app = create_app()

with app.app_context():
    # Check if empty
    if User.query.first() is None:
        # Admin
        admin_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', email='admin@skillsher.com', password_hash=admin_pw, role='admin')
        
        # Employer
        emp_pw = bcrypt.generate_password_hash('emp123').decode('utf-8')
        employer = User(username='TechCorp', email='hr@techcorp.com', password_hash=emp_pw, role='employer')
        
        # Fresher
        fresh_pw = bcrypt.generate_password_hash('fresh123').decode('utf-8')
        fresher = User(username='johndoe', email='john@example.com', password_hash=fresh_pw, role='fresher')
        
        db.session.add_all([admin, employer, fresher])
        db.session.commit()
        
        # Course
        course = Course(title='Full-Stack Masterclass', description='Learn to build end-to-end web platforms.', url='https://docs.python.org/', category='Web Development')
        db.session.add(course)
        
        # Job
        job = Job(title='Junior Python Engineer', description='Seeking a passionate entry-level engineer to join our dynamic team.', requirements='Python, Flask, Basic SQL, Git.', location='Remote', salary='$55,000 - $70,000', employer_id=employer.id)
        db.session.add(job)
        
        db.session.commit()
        print("Database seeded successfully!")
    else:
        print("Database already seeded.")
