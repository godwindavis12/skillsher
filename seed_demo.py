import os
from datetime import datetime, timedelta
from app import create_app, db, bcrypt
from app.models import User, Job, Course, Application

app = create_app()

with app.app_context():
    print("Dropping existing database tables...")
    db.drop_all()
    print("Creating new database tables...")
    db.create_all()

    # 1. Create Users
    print("Seeding Users...")
    
    # Admin
    admin_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
    admin = User(username='admin', email='admin@skillsher.com', password_hash=admin_pw, role='admin', full_name='System Admin')
    
    # Employers (Companies)
    emp_pw = bcrypt.generate_password_hash('emp123').decode('utf-8')
    employer1 = User(
        username='TechCorp', 
        email='hr@techcorp.com', 
        password_hash=emp_pw, 
        role='employer',
        company_name='TechCorp Inc.',
        bio='We are a leading software company building next-generation AI tools.',
        profile_image='default.jpg'
    )
    
    employer2 = User(
        username='DataMinds', 
        email='careers@dataminds.com', 
        password_hash=emp_pw, 
        role='employer',
        company_name='DataMinds Analytics',
        bio='Transforming data into insights. Join our data science revolution.',
        profile_image='default.jpg'
    )

    # Freshers
    fresh_pw = bcrypt.generate_password_hash('fresh123').decode('utf-8')
    fresher1 = User(
        username='johndoe', 
        email='john@example.com', 
        password_hash=fresh_pw, 
        role='fresher',
        full_name='John Doe',
        skills='Python, JavaScript, React, SQL',
        education='B.Sc. Computer Science, University of Technology (2020-2024)',
        experience='6 months internship at WebDev Solutions',
        bio='A passionate software developer looking for exciting opportunities.',
        profile_image='default.jpg'
    )

    fresher2 = User(
        username='janedoe', 
        email='jane@example.com', 
        password_hash=fresh_pw, 
        role='fresher',
        full_name='Jane Doe',
        skills='Data Analysis, Python, Pandas, Machine Learning',
        education='B.Sc. Data Science, State University (2020-2024)',
        experience='Academic projects in predictive modeling',
        bio='Aspiring Data Scientist with a strong mathematical background.',
        profile_image='default.jpg'
    )

    db.session.add_all([admin, employer1, employer2, fresher1, fresher2])
    db.session.commit()

    # 2. Create Courses
    print("Seeding Courses...")
    course1 = Course(
        title='Full-Stack Masterclass', 
        description='Learn to build end-to-end web platforms using Python and React.', 
        url='https://docs.python.org/', 
        category='Web Development',
        employer_id=employer1.id
    )
    
    course2 = Course(
        title='Data Science Bootcamp', 
        description='Master data analysis, visualization, and machine learning.', 
        url='https://pandas.pydata.org/docs/', 
        category='Data Science',
        employer_id=employer2.id
    )
    
    course3 = Course(
        title='General Interview Prep', 
        description='Prepare for behavioral and technical interviews.', 
        url='https://example.com/interview', 
        category='Career',
        employer_id=admin.id
    )

    db.session.add_all([course1, course2, course3])
    db.session.commit()

    # 3. Create Jobs
    print("Seeding Jobs...")
    job1 = Job(
        title='Junior Python Engineer', 
        description='Seeking a passionate entry-level engineer to join our dynamic team.', 
        requirements='Python, Flask, Basic SQL, Git.', 
        location='Remote', 
        salary='$55,000 - $70,000', 
        employer_id=employer1.id,
        posted_at=datetime.utcnow() - timedelta(days=2)
    )
    # Link course to job
    job1.courses.append(course1)
    job1.courses.append(course3)

    job2 = Job(
        title='Data Analyst Fresher', 
        description='Looking for a bright mind to analyze complex datasets.', 
        requirements='Python, Pandas, SQL, strong analytical skills.', 
        location='New York, NY', 
        salary='$60,000 - $75,000', 
        employer_id=employer2.id,
        posted_at=datetime.utcnow() - timedelta(days=1)
    )
    job2.courses.append(course2)

    job3 = Job(
        title='Frontend React Developer', 
        description='Build beautiful user interfaces taking design mockups to reality.', 
        requirements='React, JavaScript, HTML, CSS.', 
        location='San Francisco, CA', 
        salary='$70,000 - $85,000', 
        employer_id=employer1.id,
        posted_at=datetime.utcnow()
    )

    db.session.add_all([job1, job2, job3])
    db.session.commit()

    # 4. Create Applications
    print("Seeding Applications...")
    app1 = Application(
        job_id=job1.id, 
        fresher_id=fresher1.id, 
        status='pending',
        is_viewed=True,  # Employer has seen this
        applied_at=datetime.utcnow() - timedelta(days=1)
    )
    
    app2 = Application(
        job_id=job2.id, 
        fresher_id=fresher2.id, 
        status='pending',
        is_viewed=False,
        applied_at=datetime.utcnow()
    )

    db.session.add_all([app1, app2])
    db.session.commit()

    print("Database seeded successfully with demo data!")
