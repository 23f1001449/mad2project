from flask import Flask, request, jsonify
from flask_mail import Mail
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from flask_migrate import Migrate
from models import db, User
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, create_access_token
from routes.student_routes import student_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from scheduler import start_scheduler
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
CORS(app,
    resources={r"/*": {"origins": "http://localhost:5173"}},
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        return jsonify({"message": "preflight ok"}), 200
app.config['SECRET_KEY'] = 'secret_key'
app.config['JWT_SECRET_KEY'] = 'this-is-a-very-long-secret-key-for-your-project-2026'
app.config["JWT_TOKEN_LOCATION"] = ["headers"]






from flask_mail import Mail, Message


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_app_password"
app.config["MAIL_DEFAULT_SENDER"] = "your_email@gmail.com"

# db = SQLAlchemy()
# db.init_app(app)
mail = Mail(app)

start_scheduler(app, mail)


@app.route("/testmail")
def test_mail():
    msg = Message(
        subject="Test Email",
        recipients=["student1@gmail.com"],
        body="Hello! This is a test email from the placement portal."
    )

    mail.send(msg)
    return "Mail sent"

jwt = JWTManager(app)

login_manager = LoginManager()
migrate = Migrate(app, db)
login_manager.init_app(app)
login_manager.login_view = 'login'
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(company_bp)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Unauthorized access'}), 401

@login_manager.user_loader
def load_user(user_id): 
    try:
        return User.query.get(int(user_id))
    except:
        return None 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

from models import db, User
db.init_app(app)        

def create_admin():
    print("Running create_admin()")

    admin = User.query.filter_by(role="admin").first()

    if admin:
        print("Admin already exists:", admin)
    else:
        print("Creating admin...")

        admin = User(
            username="admin",
            email="admin@iitm.com",
            role="admin"
        )

        admin.set_password("admin")

        db.session.add(admin)
        db.session.commit()

        print("Admin created")

with app.app_context():
    create_admin()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'User already exists'}), 400
    
    role = data.get("role", "student")   # default student

    if role not in ["student", "company"]:
        return jsonify({"error": "Invalid role"}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.update_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201




@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if not user.check_password(password):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    if not user.is_active:
        return jsonify({"message": "Account is deactivated. Please contact admin."}), 403
    
    return jsonify({
        "access_token": access_token,
        "role": user.role
    }), 200
    

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        if not current_user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin_panel():
    return jsonify({'message': 'Welcome to the admin panel'}), 200


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/profile', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200



@app.route('/allusers', methods=['GET'])
@jwt_required()
def get_all_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'role': u.role
    } for u in users]), 200

@app.route("/updateprofile", methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.update_password(data['password'])

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200

@app.route('/user/<int:user_id>', methods=['GET','DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }), 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/deleteprofile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Profile deleted successfully'}), 200

@app.route('/user/<int:user_id>/deactivate', methods=['PUT'])  
@jwt_required()
def deactivate_user(user_id):   
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    if not current_user.is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.is_active = False
    db.session.commit()
    return jsonify({'message': 'User deactivated successfully'}), 200


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    return jsonify({'message': 'This is a protected route'}), 200


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)






