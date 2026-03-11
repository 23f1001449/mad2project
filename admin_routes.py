from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from models import db, User, Company, PlacementDrive, Application, StudentProfile

admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/admin/companies', methods=['GET'])
@jwt_required()
def get_pending_companies():
    
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin.is_admin():
        return {"error": "Admin access required"}, 403

    companies = Company.query.filter_by(approval_status="pending").all()
    result = []
    for company in companies:
        result.append({
            "id": company.id,
            "company_name": company.company_name,
            "hr_contact": company.hr_contact,
            "website": company.website
        })
    return jsonify(result)
    
@admin_bp.route('/admin/company/<int:id>/approve', methods=['PUT', 'OPTIONS'])
@jwt_required()
def approve_company(id):

    if request.method == "OPTIONS":
        return "", 200
    
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin.is_admin():
        return {"error": "Admin access required"}, 403

    company = Company.query.get(id)

    if not company:
        return {"error": "Company not found"}, 404
    
    company.approval_status = "approved"
    db.session.commit()

    return {"message": "Company approved"}

@admin_bp.route('/admin/drives', methods=['GET'])
@jwt_required()
def get_pending_drives():

    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin:
        return {"error": "Admin not found"}, 404
    
    if not admin.is_admin():
        return {"error": "Admin access required"}, 403

    drives = PlacementDrive.query.filter_by(status="pending").all()

    for d in drives:
        company = Company.query.get(d.company_id)

    result = []
    for d in drives:
        result.append({
            "id": d.id,
            "company_name": company.company_name,
            "job_title": d.job_title,
            "branch": d.branch,
            "cgpa_required": d.cgpa_required,
            "deadline": d.deadline.strftime("%Y-%m-%d %H:%M")
        })

    return jsonify(result)

@admin_bp.route('/admin/drive/<int:id>/approve', methods=['PUT'])
@jwt_required()
def approve_drive(id):

    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin.is_admin():
        return {"error": "Admin access required"}, 403

    drive = PlacementDrive.query.get(id)

    if not drive:
        return {"error": "Drive not found"}, 404

    drive.status = "approved"
    db.session.commit()

    return {"message": "Placement drive approved"}


@admin_bp.route('/search/students', methods=['GET'])
@jwt_required()
def search_students():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin.is_admin():
        return {"error": "Admin access required"}, 403
    query = request.args.get('q')

    students = db.session.query(StudentProfile, User)\
        .join(User, StudentProfile.user_id == User.id)\
        .filter(
            (StudentProfile.full_name.ilike(f"%{query}%")) |
            (StudentProfile.branch.ilike(f"%{query}%")) |
            (StudentProfile.skills.ilike(f"%{query}%")) |
            (User.email.ilike(f"%{query}%"))
        ).all()

    result = []

    for profile, user in students:
        result.append({
            "student_id": profile.id,
            "full_name": profile.full_name,
            "email": user.email,
            "branch": profile.branch,
            "cgpa": profile.cgpa,
            "skills": profile.skills
        })

    return jsonify(result), 200



@admin_bp.route('/search/companies', methods=['GET'])
@jwt_required()
def search_companies():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin.is_admin():
        return {"error": "Admin access required"}, 403
    query = request.args.get('q')

    companies = Company.query.filter(
        Company.company_name.ilike(f"%{query}%")
    ).all()

    result = []

    for company in companies:
        result.append({
            "company_id": company.id,
            "name": company.company_name,
            "website": company.website,
            "hr_contact": company.hr_contact,
        })

    return jsonify(result), 200



@admin_bp.route('/reports/statistics', methods=['GET'])
@jwt_required()
def placement_statistics():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin.is_admin():
        return {"error": "Admin access required"}, 403
    total_students = StudentProfile.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()

    selected_students = Application.query.filter_by(status="Selected").count()

    # Applications per company
    company_stats = db.session.query(
        Company.company_name,
        func.count(Application.id)
    ).join(
        PlacementDrive, PlacementDrive.company_id == Company.id
    ).join(
        Application, Application.drive_id == PlacementDrive.id
    ).group_by(
        Company.company_name
    ).all()

    applications_per_company = []

    for company, count in company_stats:
        applications_per_company.append({
            "company": company,
            "applications": count
        })

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives,
        "total_applications": total_applications,
        "selected_students": selected_students,
        "applications_per_company": applications_per_company
    }), 200


