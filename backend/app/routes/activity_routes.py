from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import mongo

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/user-activity/', methods=['GET'])
@jwt_required()
def user_activity():
    email = get_jwt_identity()
    resumes_uploaded = mongo.db.resumes.count_documents({'user_email': email})
    ats_scores = mongo.db.ats_scores.count_documents({'user_email': email})
    improvements = mongo.db.improvements.count_documents({'user_email': email})
    return jsonify({
        'resumes_uploaded': resumes_uploaded,
        'ats_scores': ats_scores,
        'improvements': improvements
    }), 200 