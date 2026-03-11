from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from flask_sqlalchemy import SQLAlchemy

# from django.db import models

db = SQLAlchemy()

IST = ZoneInfo("Asia/Kolkata")

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(
        db.Enum('admin', 'student', 'company', name='user_roles'),
        nullable=False,
        default='student'
    )
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime(timezone=True))
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(IST), onupdate=lambda: datetime.now(IST))
    #utcnow to indian time

    #password handling
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def update_password(self, password):
        self.password_hash = generate_password_hash(password)
    

    #role helper
    def is_admin(self):
        return self.role == 'admin'
    
    def is_student(self):
        return self.role == 'student'

    def is_company(self):
        return self.role == 'company'
    
    def __repr__(self):
        return f'<User {self.username}>'



class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    full_name = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    skills = db.Column(db.String(300))
    resume = db.Column(db.String(200))

    user = db.relationship('User', backref='student_profile')


class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    hr_contact = db.Column(db.String(120))
    website = db.Column(db.String(200))

    approval_status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(IST))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(IST), onupdate=lambda: datetime.now(IST))

    def __repr__(self):
        return f'<Company {self.name}>'
    

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profiles.id'))
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'))

    application_date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(IST))

    status = db.Column(db.String(20), default="Applied")

    interview_date = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f'<Application User:{self.student_id} Drive:{self.drive_id}>'    
    

class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    job_title = db.Column(db.String(200))
    job_description = db.Column(db.Text)

    branch = db.Column(db.String(50))
    cgpa_required = db.Column(db.Float)

    deadline = db.Column(db.DateTime)

    status = db.Column(db.String(20), default="pending")    