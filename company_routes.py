from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models import Company, PlacementDrive, User, db, Application, StudentProfile
from datetime import datetime, timezone, timedelta
from datetime import datetime
from zoneinfo import ZoneInfo

IST = timezone(timedelta(hours=5, minutes=30))

company_bp = Blueprint('company', __name__)

@company_bp.route('/company/register', methods=['POST'])
@jwt_required()
def register_company():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user.role != "company":
        return {"error": "Only company accounts can register companies"}, 403

    data = request.get_json()

    company = Company(
        user_id=user_id,
        company_name=data["company_name"],
        hr_contact=data["hr_contact"],
        website=data["website"]
    )

    db.session.add(company)
    db.session.commit()

    return {"message": "Company registration submitted for approval"}



@company_bp.route('/drive/create', methods=['POST'])
@jwt_required()
def create_drive():

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    company = Company.query.filter_by(user_id=user_id).first()

    if user.role != "company":
        return {"error": "Only companies can create drives"}, 403

    if not company:
        return {"error": "Company profile not found"}, 404

    if company.approval_status != "approved":
        return {"error": "Company registration is pending approval"}, 403
    
    if not company:
        return {"error": "Company profile not found"}, 404
    
    if company.approval_status != "approved":
        return {"error": "Company not approved yet"}, 403
    
    data = request.get_json()

    deadline=datetime.strptime(data["deadline"], "%Y-%m-%d %H:%M")
    deadline = deadline.replace(tzinfo=ZoneInfo("Asia/Kolkata"))

    drive = PlacementDrive(
        company_id=company.id,
        job_title=data["job_title"],
        job_description=data["job_description"],
        branch=data["branch"],
        cgpa_required=data["cgpa_required"],
        deadline=deadline
    )

    db.session.add(drive)
    db.session.commit()

    return {"message": "Drive created and waiting for admin approval"}


@company_bp.route('/company/applications', methods=['GET'])
@jwt_required()
def view_applications():

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return {"error": "Company profile not found"}, 404

    if company.approval_status != "approved":
        return {"error": "Company registration is pending approval"}, 403

    drives = PlacementDrive.query.filter_by(company_id=company.id).all()

    result = []

    for drive in drives:
        applications = Application.query.filter_by(drive_id=drive.id).all()

        for app in applications:
            profile = StudentProfile.query.get(app.student_id)
            student = User.query.get(profile.user_id)

            result.append({
                "application_id": app.id,
                "student_id": student.id,
                "student_name": student.username,
                "drive_id": drive.id,
                "job_title": drive.job_title,
                "status": app.status
            })

    return jsonify(result), 200


@company_bp.route('/application/<int:app_id>/status', methods=['PUT'])
@jwt_required()
def update_application_status(app_id):

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return {"error": "Company not found"}, 404

    application = Application.query.get(app_id)

    if not application:
        return {"error": "Application not found"}, 404

    drive = PlacementDrive.query.get(application.drive_id)

    if drive.company_id != company.id:
        return {"error": "Not authorized"}, 403

    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Shortlisted", "Rejected", "Selected"]:
        return {"error": "Invalid status"}, 400

    application.status = new_status
    db.session.commit()

    return {"message": "Application status updated"}



@company_bp.route('/application/<int:app_id>/scheduleinterview', methods=['PUT'])
@jwt_required()
def schedule_interview(app_id):

    user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return {"error": "Company not found"}, 404

    application = Application.query.get(app_id)
    if not application:
        return {"error": "Application not found"}, 404

    drive = PlacementDrive.query.get(application.drive_id)

    if drive.company_id != company.id:
        return {"error": "Not authorized"}, 403

    data = request.get_json()

    interview_date = datetime.strptime(data["interview_date"], "%Y-%m-%d %H:%M")
    interview_date = interview_date.replace(tzinfo=ZoneInfo("Asia/Kolkata"))

    application.interview_date = interview_date
    application.status = "Interview Scheduled"

    db.session.commit()

    return {"message": "Interview scheduled successfully"}
