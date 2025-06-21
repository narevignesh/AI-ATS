from sentence_transformers import SentenceTransformer, util
from flask import Blueprint, request, jsonify
import numpy as np
from flask_jwt_extended import jwt_required, get_jwt_identity

suggest_bp = Blueprint('suggest', __name__)

# Load the model once globally
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_keywords(text):
    words = set(w.lower().strip(",.()[]{}:;") for w in text.split() if len(w) > 3)
    return words

@suggest_bp.route('/get-suggestions/', methods=['POST'])
@jwt_required()
def get_suggestions():
    data = request.json
    resume_section = data.get('resume_section', '')
    job_description = data.get('job_description', '')
    if not resume_section or not job_description:
        return jsonify({'msg': 'Resume section and JD required'}), 400
    
    try:
        resume_keywords = extract_keywords(resume_section)
        jd_keywords = extract_keywords(job_description)
        missing_keywords = list(jd_keywords - resume_keywords)

        # Rank missing keywords by semantic similarity to resume section
        resume_emb = model.encode([resume_section])[0]
        keyword_scores = []
        for kw in missing_keywords:
            kw_emb = model.encode([kw])[0]
            sim = float(np.dot(resume_emb, kw_emb) / (np.linalg.norm(resume_emb) * np.linalg.norm(kw_emb)))
            keyword_scores.append((kw, sim))
        keyword_scores.sort(key=lambda x: -x[1])
        top_keywords = [kw for kw, _ in keyword_scores[:10]]

        # For each top keyword, generate a professional sentence
        keyword_sentences = [
            f"Demonstrated expertise in {kw} to drive project success and deliver measurable results."
            for kw in top_keywords
        ]

        improved_content = resume_section.strip()
        if keyword_sentences:
            improved_content += "\n\n" + "\n".join(keyword_sentences)

        # Use top 2 missing keywords for dynamic examples
        example_kw1 = top_keywords[0] if len(top_keywords) > 0 else 'key skill'
        example_kw2 = top_keywords[1] if len(top_keywords) > 1 else 'another skill'

        improvement_tips = [
            f"Tailor your resume section to the job description. For example, if the JD emphasizes '{example_kw1}', make sure to highlight your experience with it.",
            f"Use quantifiable results: e.g., 'Increased efficiency by 20% using {example_kw1}.'",
            f"Start each bullet with a strong action verb: e.g., 'Implemented {example_kw2} to streamline processes.'",
            f"Mirror the language of the job description. If the JD uses phrases like '{example_kw1}' or '{example_kw2}', use them in your resume if relevant.",
            f"Highlight leadership, initiative, and problem-solving skills, especially in the context of {example_kw1} or {example_kw2}.",
            "Keep bullet points concise and focused on your impact, not just your duties.",
            "If the job description mentions specific tools or technologies, ensure they are included if you have experience with them.",
            "Prioritize the most relevant skills and experiences for the target role.",
            "Proofread for clarity, grammar, and professionalism."
        ]

        # Log activity
        user_email = get_jwt_identity()
        from app.extensions import mongo
        from datetime import datetime
        mongo.db.improvements.insert_one({
            'user_email': user_email,
            'created_at': datetime.utcnow()
        })
        
        return jsonify({
            'improved_content': improved_content,
            'missing_keywords': top_keywords,
            'improvement_tips': improvement_tips
        }), 200
        
    except Exception as e:
        return jsonify({'msg': f'Local suggestion error: {str(e)}'}), 500 