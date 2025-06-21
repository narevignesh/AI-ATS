from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

def user_dict(user):
    return {
        'id': str(user['_id']),
        'name': user['name'],
        'email': user['email'],
        'role': user.get('role', 'user'),
        'auth_type': user.get('auth_type', 'email'),
        'is_verified': user.get('is_verified', False)
    }

def create_user(mongo, name, email, password, role='user', auth_type='email', is_verified=False, is_hashed=False):
    password_hash = password if is_hashed else generate_password_hash(password)
    user = {
        'name': name,
        'email': email,
        'password_hash': password_hash,
        'role': role,
        'auth_type': auth_type,
        'is_verified': is_verified
    }
    mongo.db.users.insert_one(user)
    return user

def find_user_by_email(mongo, email):
    return mongo.db.users.find_one({'email': email})

def verify_password(user, password):
    return check_password_hash(user['password_hash'], password) 