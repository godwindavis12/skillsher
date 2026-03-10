# Skill Sher - Hiring Platform

A comprehensive hiring platform built with Python, Flask, and SQLite. Skill Sher connects employers with fresh talent, featuring job boards, course management, dynamic candidate profiles, AI-powered job recommendations, and seamless application tracking.

## Features

- **Multi-Role Authentication**: Distinct dashboards and capabilities for Admin, Employer, and Fresher roles.
- **Job Management**: Employers can post, edit, and delete job listings, and link required learning courses to specific roles.
- **Company Profiles & Courses**: Employers can create public company profiles, upload custom courses with materials, and showcase open positions.
- **Candidate Profiles**: Freshers can build detailed profiles including skills, experience, education, bio, and a profile picture.
- **AI Job Recommendations**: A keyword-matching AI engine recommends jobs to freshers based on their specified skills.
- **Application Tracking**: Employers can view applications (automatically updating the applicant's status to "Viewed").
- **Global Search**: Search across all jobs, courses, and companies directly from the navigation bar.

## Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy (ORM), Flask-Login (Authentication), Flask-Bcrypt (Password Hashing)
- **Frontend:** HTML5, CSS3 (Custom Design System, Flexbox/Grid layouts), Jinja2 Templating
- **Database:** SQLite (Development)

## Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skill-sher.git
   cd skill-sher
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Create a `.env` file in the root directory (optional but recommended for production):
   ```env
   SECRET_KEY=your_secure_secret_key_here
   FLASK_APP=run.py
   FLASK_ENV=development
   ```

5. **Initialize to Database (Demo Data)**
   A script is provided to automatically create the database tables and populate them with demo users, companies, jobs, courses, and applications.
   ```bash
   python seed_demo.py
   ```

6. **Run the Application**
   ```bash
   python run.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## Demo Credentials

If you ran `seed_demo.py`, you can use the following accounts to explore the platform:

**Employers (Companies)**
- Email: `hr@techcorp.com` | Password: `emp123`
- Email: `careers@dataminds.com` | Password: `emp123`

**Freshers (Candidates)**
- Email: `john@example.com` | Password: `fresh123`
- Email: `jane@example.com` | Password: `fresh123`

**Admin**
- Email: `admin@skillsher.com` | Password: `admin123`

## Project Structure
```text
skill_sher/
├── app/
│   ├── __init__.py       # App factory & config initialization
│   ├── models.py         # SQLAlchemy Database Models
│   ├── routes/           # Blueprints for different user roles
│   │   ├── auth.py       
│   │   ├── main.py       
│   │   ├── employer.py   
│   │   ├── fresher.py    
│   │   └── admin.py      
│   ├── static/           # CSS, JS, and uploaded files (profiles, courses)
│   └── templates/        # Jinja2 HTML templates
├── run.py                # Application entry point
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── seed_demo.py          # Script to populate the database with mock data
```

## License
This project is open-source and available under the [MIT License](LICENSE).
