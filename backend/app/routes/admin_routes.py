from flask import Blueprint, jsonify, request, send_file, make_response
from app.extensions import mongo
from app.utils.role_required import role_required
from flask_jwt_extended import jwt_required
from bson import ObjectId
import csv
from io import StringIO
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users/', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    users = list(mongo.db.users.find())
    for u in users:
        u['id'] = str(u['_id'])
        u.pop('_id', None)
        u.pop('password_hash', None)
    return jsonify({'users': users}), 200

@admin_bp.route('/resumes/', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_resumes():
    resumes = list(mongo.db.resumes.find())
    for r in resumes:
        r['id'] = str(r['_id'])
        r.pop('_id', None)
    return jsonify({'resumes': resumes}), 200

@admin_bp.route('/delete-user/<id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'User deleted'}), 200

# New: Get all user activities
@admin_bp.route('/all-activities/', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_activities():
    users = list(mongo.db.users.find())
    activities = []
    for u in users:
        email = u['email']
        resumes_uploaded = mongo.db.resumes.count_documents({'user_email': email})
        ats_scores = mongo.db.ats_scores.count_documents({'user_email': email})
        improvements = mongo.db.improvements.count_documents({'user_email': email})
        activities.append({
            'name': u.get('name'),
            'email': email,
            'role': u.get('role'),
            'verified': u.get('is_verified', False),
            'resumes_uploaded': resumes_uploaded,
            'ats_scores': ats_scores,
            'improvements': improvements
        })
    return jsonify({'activities': activities}), 200

# New: Get all resumes with user info
@admin_bp.route('/all-resumes/', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_resumes():
    resumes = list(mongo.db.resumes.find())
    users = {u['email']: u for u in mongo.db.users.find()}
    result = []
    for r in resumes:
        user = users.get(r.get('user_email'))
        r_out = {k: v for k, v in r.items() if k != '_id'}
        r_out['id'] = str(r['_id'])
        if user:
            r_out['user'] = {
                'name': user.get('name'),
                'email': user.get('email'),
                'role': user.get('role'),
                'verified': user.get('is_verified', False)
            }
        result.append(r_out)
    return jsonify({'resumes': result}), 200

@admin_bp.route('/export-logs', methods=['GET'])
@jwt_required()
@role_required('admin')
def export_logs():
    # Fetch all user activities
    users = list(mongo.db.users.find())
    activities = []
    for u in users:
        email = u['email']
        resumes_uploaded = mongo.db.resumes.count_documents({'user_email': email})
        ats_scores = mongo.db.ats_scores.count_documents({'user_email': email})
        improvements = mongo.db.improvements.count_documents({'user_email': email})
        activities.append({
            'name': u.get('name'),
            'email': email,
            'role': u.get('role'),
            'verified': u.get('is_verified', False),
            'resumes_uploaded': resumes_uploaded,
            'ats_scores': ats_scores,
            'improvements': improvements
        })
    # Fetch all resumes
    resumes = list(mongo.db.resumes.find())
    users_map = {u['email']: u for u in users}
    resumes_out = []
    for r in resumes:
        user = users_map.get(r.get('user_email'))
        r_out = {k: v for k, v in r.items() if k != '_id'}
        r_out['id'] = str(r['_id'])
        if user:
            r_out['user_name'] = user.get('name')
            r_out['user_email'] = user.get('email')
            r_out['user_role'] = user.get('role')
            r_out['user_verified'] = user.get('is_verified', False)
        resumes_out.append(r_out)
    # Write to CSV
    output = StringIO()
    writer = csv.writer(output)
    # Write activities table
    writer.writerow(['User Activities'])
    writer.writerow(['Name', 'Email', 'Role', 'Verified', 'Resumes Uploaded', 'ATS Scores', 'Improvements'])
    for a in activities:
        writer.writerow([a['name'], a['email'], a['role'], 'Yes' if a['verified'] else 'No', a['resumes_uploaded'], a['ats_scores'], a['improvements']])
    writer.writerow([])
    writer.writerow(['---'])
    writer.writerow([])
    # Write resumes table
    writer.writerow(['Resumes'])
    writer.writerow(['ID', 'Filename', 'User Name', 'User Email', 'User Role', 'User Verified'])
    for r in resumes_out:
        writer.writerow([r.get('id'), r.get('filename'), r.get('user_name', '-'), r.get('user_email', '-'), r.get('user_role', '-'), 'Yes' if r.get('user_verified') else 'No'])
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=ats_logs_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response 