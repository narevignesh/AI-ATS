﻿# AI-ATS Resume System - Backend

## 🚀 Overview
A robust Flask-based backend API for the AI-ATS Resume System, providing comprehensive resume parsing, ATS scoring, AI-powered suggestions, and user management with secure authentication.

## 🧰 Tech Stack
- **Framework:** Flask 3.1.1
- **Database:** MongoDB with PyMongo
- **Authentication:** JWT, OTP
- **Email:** Flask-Mail with Gmail SMTP
- **AI/ML:** sentence-transformers, scikit-learn
- **File Processing:** PyMuPDF, docx2txt
- **Security:** Flask-JWT-Extended, python-decouple

## 📁 Project Structure
```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extensions setup
│   ├── models/
│   │   └── user_model.py    # User data model
│   ├── routes/
│   │   ├── auth_routes.py   # Authentication endpoints
│   │   ├── resume_routes.py # Resume upload/parse
│   │   ├── ats_routes.py    # ATS scoring
│   │   ├── suggest_routes.py # AI suggestions
│   │   ├── admin_routes.py  # Admin dashboard
│   │   └── activity_routes.py # User activity
│   └── utils/
│       ├── email_utils.py   # Email functionality
│       ├── role_required.py # Role-based access
│       └── token_utils.py   # JWT utilities
├── uploads/                 # Resume file storage
├── venv/                   # Virtual environment
├── requirements.txt        # Python dependencies
├── env_template.txt        # Environment template
├── run.py                 # Application entry point
└── README.md              # This file
```

## ⚙️ Installation & Setup

### 1. Prerequisites
- Python 3.8+
- MongoDB installed and running
- Gmail account with App Password
- **Frontend:** Node.js 18+ (for full-stack development)

### 2. Environment Setup
```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Create `.env` file:
```env
# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/ATS

# Email Configuration
MAIL_USERNAME=your-actual-gmail@gmail.com
MAIL_PASSWORD=your-16-character-gmail-app-password

# CORS Configuration
CORS_ORIGINS=http://localhost:8080,http://localhost:3000
```

### 4. Gmail App Password Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account > Security > 2-Step Verification > App passwords
3. Select "Mail" and "Other (Custom name)" - name it "ATS Resume Tool"
4. Copy the 16-character password (remove spaces)

### 5. Run the Application
```bash
python run.py
```
Server will start at `http://localhost:5000`

## 📦 Dependencies

### Backend Dependencies (`requirements.txt`)
All Python dependencies are listed in `requirements.txt`:
- **Flask 3.1.1** - Web framework
- **Flask-JWT-Extended 4.7.1** - JWT authentication
- **Flask-Mail 0.10.0** - Email functionality
- **Flask-CORS** - Cross-origin resource sharing
- **Flask-PyMongo** - MongoDB integration
- **PyMuPDF** - PDF processing
- **docx2txt** - DOCX processing
- **sentence-transformers** - AI embeddings
- **scikit-learn** - Machine learning utilities

### Frontend Dependencies
For frontend development, see the following files in the `frontend/` directory:
- **`frontend/requirements.txt`** - Human-readable dependency list
- **`frontend/package-requirements.json`** - Package.json format for easy installation
- **`frontend/app/package.json`** - Actual package.json with scripts

**Core Frontend Dependencies:**
- React 18.3.1 - UI framework
- Vite 5.4.1 - Build tool
- Tailwind CSS 3.4.11 - Styling
- shadcn/ui - UI components
- Chart.js 4.5.0 - Data visualization
- Axios 1.10.0 - HTTP client

**Frontend Installation:**
```bash
# Navigate to frontend directory
cd frontend/app

# Install dependencies
npm install

# Alternative: Use requirements file
cd frontend
npm install --package-lock-only
npm ci

# Run
npm run dev
```

## 🔐 Authentication System

### JWT Token Management
- Access tokens expire in 1 hour
- Refresh tokens expire in 30 days
- Automatic token refresh on API calls

### OTP Verification
- 6-digit OTP sent via email
- OTP expires in 10 minutes
- Rate limiting: 3 attempts per 15 minutes

## 📊 Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "name": "string",
  "email": "string (unique)",
  "password": "string (hashed)",
  "role": "user|admin",
  "is_verified": "boolean",
  "created_at": "datetime",
  "last_login": "datetime"
}
```

### Resumes Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "filename": "string",
  "file_path": "string",
  "parsed_data": {
    "name": "string",
    "email": "string",
    "phone": "string",
    "skills": ["string"],
    "experience": ["string"],
    "education": ["string"]
  },
  "ats_score": "number",
  "created_at": "datetime"
}
```

### Activities Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "activity_type": "resume_upload|ats_score|improvement",
  "description": "string",
  "created_at": "datetime"
}
```

## 🔌 API Endpoints

### Authentication Endpoints

#### 1. User Registration
```http
POST /api/signup/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```
**Response:**
```json
{
  "message": "Registration successful. Please check your email for OTP verification.",
  "user_id": "user_id_here"
}
```

#### 2. OTP Verification
```http
POST /api/verify-otp/
Content-Type: application/json

{
  "email": "john@example.com",
  "otp": "123456"
}
```
**Response:**
```json
{
  "message": "OTP verified successfully",
  "access_token": "jwt_token_here",
  "refresh_token": "refresh_token_here"
}
```

#### 3. User Login
```http
POST /api/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "securepassword123"
}
```
**Response:**
```json
{
  "message": "Login successful",
  "access_token": "jwt_token_here",
  "refresh_token": "refresh_token_here",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

#### 4. Forgot Password
```http
POST /api/forgot-password/
Content-Type: application/json

{
  "email": "john@example.com"
}
```
**Response:**
```json
{
  "message": "Password reset OTP sent to your email"
}
```

#### 5. Validate Reset OTP
```http
POST /api/validate-reset-otp/
Content-Type: application/json

{
  "email": "john@example.com",
  "otp": "123456"
}
```
**Response:**
```json
{
  "message": "OTP validated successfully",
  "reset_token": "reset_token_here"
}
```

#### 6. Reset Password
```http
POST /api/reset-password/
Content-Type: application/json

{
  "email": "john@example.com",
  "reset_token": "reset_token_here",
  "new_password": "newpassword123"
}
```
**Response:**
```json
{
  "message": "Password reset successfully"
}
```

### Resume Management Endpoints

#### 7. Upload Resume
```http
POST /api/upload-resume/
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data

Form Data:
- file: resume.pdf (or .docx)
```
**Response:**
```json
{
  "message": "Resume uploaded successfully",
  "filename": "resume.pdf",
  "file_id": "file_id_here"
}
```

#### 8. Parse Resume
```http
POST /api/parse-resume/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "filename": "resume.pdf"
}
```
**Response:**
```json
{
  "message": "Resume parsed successfully",
  "parsed_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "skills": ["Python", "JavaScript", "React"],
    "experience": ["Software Engineer at Tech Corp"],
    "education": ["BS Computer Science"]
  }
}
```

### ATS Scoring Endpoints

#### 9. Get ATS Score
```http
POST /api/get-ats-score/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "job_title": "Software Engineer",
  "job_description": "We are looking for a Python developer...",
  "resume_text": "John Doe is a software engineer..."
}
```
**Response:**
```json
{
  "ats_score": 85,
  "skill_match": 78.5,
  "keyword_match": 82.3,
  "missing_keywords": ["Docker", "Kubernetes"],
  "suggestions": ["Add Docker experience", "Include Kubernetes skills"]
}
```

### AI Suggestions Endpoints

#### 10. Get Resume Suggestions
```http
POST /api/get-suggestions/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "resume_text": "Current resume content...",
  "job_description": "Target job description..."
}
```
**Response:**
```json
{
  "suggestions": {
    "summary": "Improved professional summary...",
    "experience": ["Enhanced experience descriptions..."],
    "skills": ["Add relevant skills..."],
    "education": ["Improve education section..."]
  },
  "overall_score": 92
}
```

### Admin Endpoints

#### 11. Get All Users
```http
GET /api/admin/users/
Authorization: Bearer <admin_jwt_token>
```
**Response:**
```json
{
  "users": [
    {
      "id": "user_id",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "user",
      "created_at": "2024-01-01T00:00:00Z",
      "last_login": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 12. Get All Resumes
```http
GET /api/admin/resumes/
Authorization: Bearer <admin_jwt_token>
```
**Response:**
```json
{
  "resumes": [
    {
      "id": "resume_id",
      "user_name": "John Doe",
      "filename": "resume.pdf",
      "ats_score": 85,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### 13. Delete User
```http
DELETE /api/admin/delete-user/{user_id}
Authorization: Bearer <admin_jwt_token>
```
**Response:**
```json
{
  "message": "User deleted successfully"
}
```

#### 14. Get All Activities
```http
GET /api/admin/all-activities/
Authorization: Bearer <admin_jwt_token>
```
**Response:**
```json
{
  "activities": [
    {
      "id": "activity_id",
      "user_name": "John Doe",
      "activity_type": "resume_upload",
      "description": "Uploaded resume.pdf",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### User Activity Endpoints

#### 15. Get User Activity
```http
GET /api/user-activity/
Authorization: Bearer <jwt_token>
```
**Response:**
```json
{
  "total_resumes": 5,
  "total_ats_scores": 3,
  "total_improvements": 2,
  "recent_activities": [
    {
      "type": "resume_upload",
      "description": "Uploaded resume.pdf",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## 🔧 Configuration

### Flask Configuration (`config.py`)
```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
    
    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
```

## 🛡️ Security Features

### JWT Security
- Secure token generation with expiration
- Automatic token refresh
- Role-based access control

### Password Security
- Bcrypt hashing for passwords
- Password strength validation
- Secure password reset flow

### Rate Limiting
- OTP request limiting
- Login attempt limiting
- API rate limiting

### CORS Protection
- Configurable CORS origins
- Secure cross-origin requests

## 📧 Email System

### Email Templates
- Registration OTP emails
- Password reset OTP emails
- Welcome emails

### SMTP Configuration
- Gmail SMTP with App Password
- TLS encryption
- Reliable delivery

## 🤖 AI/ML Features

### ATS Scoring
- Local sentence-transformers for embeddings
- Cosine similarity scoring
- Keyword matching algorithms
- Skill relevance scoring

### Resume Parsing
- PDF parsing with PyMuPDF
- DOCX parsing with docx2txt
- Structured data extraction
- Contact information detection

### AI Suggestions
- Context-aware improvements
- Section-specific suggestions
- Keyword optimization
- Professional tone enhancement

## 📊 Monitoring & Logging

### Activity Tracking
- User action logging
- Resume upload tracking
- ATS score generation tracking
- Improvement application tracking

### Error Handling
- Comprehensive error responses
- Detailed logging
- Graceful failure handling

## 🚀 Production Deployment

### Environment Variables
```env
# Production settings
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret
MONGO_URI=mongodb://your-production-mongo-uri
CORS_ORIGINS=https://yourdomain.com
```

### Security Considerations
- Use HTTPS in production
- Secure MongoDB connection
- Environment variable protection
- Regular security updates

## 🧪 Testing

### API Testing
Use Postman or curl to test endpoints:

```bash
# Test registration
curl -X POST http://localhost:5000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'
```

## 📝 Default Admin User

The system automatically creates a default admin user:
- **Email:** vigneshnaidu022@gmail.com
- **Password:** vignesh123@MBU
- **Role:** admin

## 🔗 Dependencies

### Core Dependencies
- Flask 3.1.1 - Web framework
- Flask-JWT-Extended 4.7.1 - JWT authentication
- Flask-Mail 0.10.0 - Email functionality
- Flask-CORS - Cross-origin resource sharing
- Flask-PyMongo - MongoDB integration
- PyMuPDF - PDF processing
- docx2txt - DOCX processing
- sentence-transformers - AI embeddings
- scikit-learn - Machine learning utilities

### Development Dependencies
- python-decouple - Environment management
- requests - HTTP client
- itsdangerous - Security utilities
- werkzeug - WSGI utilities

## 📞 Support

For issues and questions:
1. Check the logs in the console
2. Verify environment variables
3. Ensure MongoDB is running
4. Check email configuration


