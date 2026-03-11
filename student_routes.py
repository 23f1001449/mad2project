from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Company, PlacementDrive, Application, StudentProfile
from scheduler import start_scheduler

student_bp = Blueprint('student', __name__)

@student_bp.route('/drives', methods=['GET'])
@jwt_required()
def get_drives():

    drives = PlacementDrive.query.filter_by(status="approved").all()

    # for d in drives:
    #     company = Company.query.get(d.company_id)

    return jsonify([
        {
            "id": d.id,
            "title": d.job_title,
            "branch": d.branch,
            "cgpa": d.cgpa_required,
            "deadline": d.deadline,
            "company_name": Company.query.get(d.company_id).company_name if Company.query.get(d.company_id) else None,
            "company_website": Company.query.get(d.company_id).website if Company.query.get(d.company_id) else None
        } for d in drives
    ]), 200

@student_bp.route('/apply/<int:drive_id>', methods=['POST'])
@jwt_required()
def apply_drive(drive_id):

    user_id = get_jwt_identity()
    
    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return {"error": "Create student profile first"}, 400

    existing = Application.query.filter_by(
        student_id=profile.id,
        drive_id=drive_id
    ).first()

    if existing:
        return {"error": "Already applied"}, 400

    app = Application(
        student_id=profile.id,
        drive_id=drive_id
    )

    db.session.add(app)
    db.session.commit()

    return {"message": "Application submitted"}


@student_bp.route('/myapplications', methods=['GET'])
@jwt_required()
def my_applications():

    user_id = get_jwt_identity()

    profile = StudentProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return {"error": "Student profile not found"}, 404
    
    applications = Application.query.filter_by(student_id=profile.id).all()

    result = []

    for app in applications:
        drive = PlacementDrive.query.get(app.drive_id)
        company = Company.query.get(drive.company_id)

        result.append({
            "application_id": app.id,
            "job_title": drive.job_title,
            "company": company.company_name,
            "status": app.status,
            "deadline": drive.deadline,
            "interview_date": app.interview_date
        })

    return jsonify(result), 200

@student_bp.route('/fulluserprofile', methods=['GET', 'POST'])
@jwt_required()
def student_profile():

    student_id = get_jwt_identity()
    user = User.query.get(student_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'POST':

        data = request.get_json()

        existing_profile = StudentProfile.query.filter_by(user_id=student_id).first()

        if existing_profile:
            return jsonify({"message": "Profile already exists"}), 400

        profile = StudentProfile(
            user_id=student_id,
            full_name=data.get("full_name"),
            branch=data.get("branch"),
            cgpa=data.get("cgpa"),
            graduation_year=data.get("graduation_year"),
            skills=data.get("skills"),
            resume=data.get("resume")
        )

        db.session.add(profile)
        db.session.commit()

        return jsonify({
            "message": "Student profile created successfully"
        }), 201


    if request.method == 'GET':

        profile = StudentProfile.query.filter_by(user_id=student_id).first()

        if not profile:
            return jsonify({"message": "Student profile not found"}), 404

        return jsonify({
            "id": profile.id,
            "full_name": profile.full_name,
            "email": user.email,
            "branch": profile.branch,
            "cgpa": profile.cgpa,
            "graduation_year": profile.graduation_year,
            "skills": profile.skills,
            "resume": profile.resume
        }), 200
    


from flask_jwt_extended import jwt_required, get_jwt_identity
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import export_applications_csv  
# from flask_mail import Message, Mail
# from app import app, mail
from extensions import mail
from flask_mail import Message
from flask import current_app

scheduler = BackgroundScheduler()
scheduler.start()

@student_bp.route("/export", methods=["POST"])
@jwt_required()
def trigger_export():
    student_id = get_jwt_identity()
    app = current_app._get_current_object()
    
    scheduler.add_job(export_applications_csv, args=[student_id, mail, app],trigger="date")
    
    return jsonify({"message": "CSV export job triggered. You will receive an email once ready."}), 200