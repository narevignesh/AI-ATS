from sentence_transformers import SentenceTransformer
import numpy as np
from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

ats_bp = Blueprint('ats', __name__)

# Load the model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode([text])[0]

def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

@ats_bp.route('/get-ats-score/', methods=['POST'])
@jwt_required()
def get_ats_score():
    data = request.json
    resume_text = data.get('resume_text', '')
    job_description = data.get('job_description', '')
    if not resume_text or not job_description:
        return jsonify({'msg': 'Resume and JD required'}), 400
    
    try:
        emb_resume = get_embedding(resume_text)
        emb_jd = get_embedding(job_description)
        ats_score = int(cosine_similarity(emb_resume, emb_jd) * 100)
        
        # Simple keyword match
        resume_words = set(resume_text.lower().split())
        jd_words = set(job_description.lower().split())
        matched = resume_words & jd_words
        skill_match = int(len(matched) / len(jd_words) * 100) if jd_words else 0
        keyword_match = skill_match
        
        # Log activity
        user_email = get_jwt_identity()
        from app.extensions import mongo
        mongo.db.ats_scores.insert_one({
            'user_email': user_email,
            'ats_score': ats_score,
            'created_at': datetime.utcnow()
        })
        
        return jsonify({
            'ats_score': ats_score,
            'skill_match': skill_match,
            'keyword_match': keyword_match
        }), 200
        
    except Exception as e:
        return jsonify({'msg': f'Local embedding error: {str(e)}'}), 500 