from flask import Blueprint, request, jsonify
from app.extensions import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import fitz  # PyMuPDF
import docx2txt
from werkzeug.utils import secure_filename
from datetime import datetime

resume_bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload-resume/', methods=['POST'])
@jwt_required()
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'msg': 'No file part'}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'msg': 'No selected file'}), 400
    if not allowed_file(file.filename):
        return jsonify({'msg': 'Invalid file type'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    user_email = get_jwt_identity()
    mongo.db.resumes.insert_one({
        'user_email': user_email,
        'filename': filename,
        'uploaded_at': datetime.utcnow(),
        'filepath': filepath
    })
    return jsonify({'msg': 'Resume uploaded', 'filename': filename}), 200

@resume_bp.route('/parse-resume/', methods=['POST'])
@jwt_required()
def parse_resume():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'msg': 'Filename required'}), 400
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({'msg': 'File not found'}), 404
    ext = filename.rsplit('.', 1)[1].lower()
    text = ''
    if ext == 'pdf':
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
    elif ext == 'docx':
        text = docx2txt.process(filepath)
    else:
        return jsonify({'msg': 'Unsupported file type'}), 400
    return jsonify({'text': text}), 200 