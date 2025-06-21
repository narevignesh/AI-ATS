from flask import Blueprint, request, jsonify, current_app, redirect, url_for, session
from app.extensions import mongo, jwt, mail
from app.models.user_model import create_user, find_user_by_email, verify_password, user_dict
from app.utils.email_utils import generate_otp, send_otp_email, create_env_file
from app.utils.token_utils import generate_reset_token, verify_reset_token
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
import datetime
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup/', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if find_user_by_email(mongo, email):
        return jsonify({'msg': 'Email already registered'}), 400
    
    try:
        # Try to create .env file if it doesn't exist
        try:
            create_env_file()
        except Exception as e:
            print(f"Could not create .env file: {str(e)}")
        
        otp = generate_otp()
        print(f"Generated OTP for {email}: {otp}")  # Debug log
        
        # Store OTP in database
        mongo.db.otp.insert_one({'email': email, 'otp': otp})
        print(f"OTP stored in database for {email}")  # Debug log
        
        # Store temp user
        mongo.db.temp_users.insert_one({'name': name, 'email': email, 'password': generate_password_hash(password)})
        print(f"Temp user stored for {email}")  # Debug log
        
        # Try to send email
        try:
            send_otp_email(mail, email, otp)
            print(f"OTP email sent successfully to {email}")  # Debug log
            return jsonify({'msg': 'OTP sent to email'}), 200
        except Exception as email_error:
            print(f"Email sending failed for {email}: {str(email_error)}")  # Debug log
            # Still create the user but mark as unverified
            create_user(mongo, name, email, password, is_verified=False)
            return jsonify({'msg': 'Account created but email verification failed. Please contact support.'}), 200
            
    except Exception as e:
        print(f"Signup error for {email}: {str(e)}")  # Debug log
        return jsonify({'msg': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/verify-otp/', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    record = mongo.db.otp.find_one({'email': email, 'otp': otp})
    if not record:
        return jsonify({'msg': 'Invalid OTP'}), 400
    temp_user = mongo.db.temp_users.find_one({'email': email})
    if not temp_user:
        return jsonify({'msg': 'User not found'}), 404
    create_user(mongo, temp_user['name'], email, temp_user['password'], is_verified=True, is_hashed=True)
    mongo.db.otp.delete_many({'email': email})
    mongo.db.temp_users.delete_many({'email': email})
    return jsonify({'msg': 'Email verified, account created'}), 200

@auth_bp.route('/resend-otp/', methods=['POST'])
def resend_otp():
    data = request.json
    email = data.get('email')
    print(f"Resend OTP requested for: {email}")  # Debug log
    
    temp_user = mongo.db.temp_users.find_one({'email': email})
    if not temp_user:
        print(f"Temp user not found for: {email}")  # Debug log
        return jsonify({'msg': 'User not found'}), 404
    
    try:
        # Delete old OTP
        mongo.db.otp.delete_many({'email': email})
        print(f"Old OTP deleted for: {email}")  # Debug log
        
        # Generate new OTP
        otp = generate_otp()
        print(f"New OTP generated for {email}: {otp}")  # Debug log
        
        # Store new OTP
        mongo.db.otp.insert_one({'email': email, 'otp': otp})
        print(f"New OTP stored for: {email}")  # Debug log
        
        # Send new OTP
        try:
            send_otp_email(mail, email, otp)
            print(f"Resend OTP email sent successfully to {email}")  # Debug log
            return jsonify({'msg': 'New OTP sent to your email'}), 200
        except Exception as email_error:
            print(f"Resend email sending failed for {email}: {str(email_error)}")  # Debug log
            return jsonify({'msg': 'Failed to send OTP. Please try again.'}), 500
            
    except Exception as e:
        print(f"Resend OTP error for {email}: {str(e)}")  # Debug log
        return jsonify({'msg': 'Failed to resend OTP'}), 500

@auth_bp.route('/login/', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    user = find_user_by_email(mongo, email)
    if not user or not verify_password(user, password):
        return jsonify({'msg': 'Invalid credentials'}), 401
    if not user.get('is_verified', False):
        return jsonify({'msg': 'Email not verified'}), 403
    access_token = create_access_token(identity=user['email'], additional_claims={'role': user.get('role', 'user')})
    return jsonify({'access_token': access_token, 'user': user_dict(user)}), 200

@auth_bp.route('/forgot-password/', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    user = find_user_by_email(mongo, email)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    try:
        otp = generate_otp()
        expiry = datetime.utcnow() + timedelta(minutes=10)
        # Store OTP for password reset
        mongo.db.reset_otps.update_one(
            {'email': email},
            {'$set': {'otp': otp, 'expires_at': expiry}},
            upsert=True
        )
        send_otp_email(mail, email, f"Your password reset OTP is: {otp}")
        return jsonify({'msg': 'Password reset OTP sent to your email.'}), 200
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return jsonify({'msg': 'Email service unavailable. Please contact support.'}), 500

@auth_bp.route('/validate-reset-otp/', methods=['POST'])
def validate_reset_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    record = mongo.db.reset_otps.find_one({'email': email, 'otp': otp})
    if not record:
        return jsonify({'msg': 'Invalid OTP'}), 400
    if record['expires_at'] < datetime.utcnow():
        return jsonify({'msg': 'OTP expired'}), 400
    # Mark OTP as validated (could set a flag or just allow next step)
    mongo.db.reset_otps.update_one({'email': email}, {'$set': {'validated': True}})
    return jsonify({'msg': 'OTP validated'}), 200

@auth_bp.route('/reset-password/', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    record = mongo.db.reset_otps.find_one({'email': email, 'validated': True})
    if not record:
        return jsonify({'msg': 'OTP not validated'}), 400
    user = find_user_by_email(mongo, email)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    mongo.db.users.update_one({'email': email}, {'$set': {'password_hash': generate_password_hash(password)}})
    # Remove OTP after successful reset
    mongo.db.reset_otps.delete_one({'email': email})
    return jsonify({'msg': 'Password reset successful'}), 200

@auth_bp.route('/reset-password/', methods=['GET'])
def reset_password_redirect():
    token = request.args.get('token')
    frontend_url = f"http://localhost:8080/reset-password?token={token}"
    return redirect(frontend_url)

@auth_bp.route('/test-email/', methods=['GET'])
def test_email():
    """Test route to check email configuration"""
    try:
        email_config = {
            'MAIL_SERVER': current_app.config.get('MAIL_SERVER'),
            'MAIL_PORT': current_app.config.get('MAIL_PORT'),
            'MAIL_USE_TLS': current_app.config.get('MAIL_USE_TLS'),
            'MAIL_USERNAME': current_app.config.get('MAIL_USERNAME'),
            'MAIL_PASSWORD': '***' if current_app.config.get('MAIL_PASSWORD') else 'Not set'
        }
        
        # Test email sending
        test_otp = generate_otp()
        send_otp_email(mail, current_app.config.get('MAIL_USERNAME'), test_otp)
        
        return jsonify({
            'msg': 'Email test successful',
            'config': email_config,
            'test_otp': test_otp
        }), 200
        
    except Exception as e:
        return jsonify({
            'msg': 'Email test failed',
            'error': str(e),
            'config': {
                'MAIL_SERVER': current_app.config.get('MAIL_SERVER'),
                'MAIL_PORT': current_app.config.get('MAIL_PORT'),
                'MAIL_USE_TLS': current_app.config.get('MAIL_USE_TLS'),
                'MAIL_USERNAME': current_app.config.get('MAIL_USERNAME'),
                'MAIL_PASSWORD': '***' if current_app.config.get('MAIL_PASSWORD') else 'Not set'
            }
        }), 500 