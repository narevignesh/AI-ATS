# AI-ATS Resume System - Full Stack Application

## 📺 Demo Video

[Demo Video.mp4](Demo%20Video.mp4)

*Click the link above to download and watch the project walkthrough video. If viewing on GitHub, download and play locally.*

## 🚀 Overview
A comprehensive, full-stack AI-powered resume analysis and improvement system that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS). The application provides real-time ATS scoring, AI-powered suggestions, and comprehensive user management with secure authentication.

## 🎯 Key Features
- **🔐 Secure Authentication** - JWT, OTP
- **📄 Resume Parsing** - PDF/DOCX upload with intelligent text extraction
- **🎯 ATS Scoring** - Real-time scoring with local AI models
- **🤖 AI Suggestions** - Context-aware resume improvements
- **📊 Analytics Dashboard** - User activity and system monitoring
- **👨‍💼 Admin Panel** - Comprehensive user and system management
- **📱 Responsive Design** - Mobile-first, modern UI
- **🔒 Security** - Role-based access, rate limiting, CORS protection

## 🏗️ Architecture

### Backend (Flask + MongoDB)
- **Framework:** Flask 3.1.1 with RESTful API
- **Database:** MongoDB with PyMongo
- **Authentication:** JWT, OTP
- **AI/ML:** sentence-transformers, scikit-learn
- **File Processing:** PyMuPDF, docx2txt
- **Email:** Flask-Mail with Gmail SMTP

### Frontend (React + Vite)
- **Framework:** React 18.3.1 with Vite 5.4.1
- **Styling:** Tailwind CSS 3.4.11 with shadcn/ui
- **Routing:** React Router DOM 7.6.2
- **Charts:** Chart.js 4.5.0 with React Chart.js 2
- **State Management:** React Query (TanStack Query)
- **Forms:** React Hook Form with Zod validation

## 📁 Project Structure
```
AI-ATS/
├── backend/                    # Flask Backend
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── config.py          # Configuration
│   │   ├── extensions.py      # Flask extensions
│   │   ├── models/
│   │   │   └── user_model.py  # User data model
│   │   ├── routes/
│   │   │   ├── auth_routes.py     # Authentication
│   │   │   ├── resume_routes.py   # Resume management
│   │   │   ├── ats_routes.py      # ATS scoring
│   │   │   ├── suggest_routes.py  # AI suggestions
│   │   │   ├── admin_routes.py    # Admin functions
│   │   │   └── activity_routes.py # User activity
│   │   └── utils/
│   │       ├── email_utils.py     # Email functionality
│   │       ├── role_required.py   # Role-based access
│   │       └── token_utils.py     # JWT utilities
│   ├── uploads/               # Resume file storage
│   ├── requirements.txt       # Python dependencies
│   ├── env_template.txt       # Environment template
│   ├── run.py                # Application entry point
│   └── README.md             # Backend documentation
├── frontend/                  # React Frontend
│   ├── app/
│   │   ├── src/
│   │   │   ├── components/
│   │   │   │   ├── Auth/         # Authentication components
│   │   │   │   ├── Resume/       # Resume management
│   │   │   │   ├── ATS/          # ATS scoring
│   │   │   │   ├── Suggestions/  # AI suggestions
│   │   │   │   ├── Admin/        # Admin dashboard
│   │   │   │   └── ui/           # shadcn/ui components
│   │   │   ├── pages/            # Application pages
│   │   │   ├── services/         # API services
│   │   │   ├── hooks/            # Custom hooks
│   │   │   └── lib/              # Utility libraries
│   │   ├── package.json          # Node dependencies
│   │   ├── vite.config.ts        # Vite configuration
│   │   └── README.md             # Frontend documentation
│   ├── requirements.txt          # Frontend dependencies list
│   ├── package-requirements.json # Frontend package requirements
│   └── package.json              # Root package.json
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## ⚙️ Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 18+** with npm/yarn
- **MongoDB** installed and running
- **Gmail account** with App Password

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd AI-ATS

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend setup
cd ../frontend/app
npm install
# Alternative: Use the requirements file
# cd ../frontend
# npm install --package-lock-only
# npm ci
```

### 2. Environment Configuration

#### Backend (.env in backend/)
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

# Optional: Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
```

#### Frontend (.env in frontend/app/)
```env
# API Configuration
VITE_API_BASE_URL=http://localhost:5000/api

# Optional: Analytics and monitoring
VITE_APP_ENV=development
```

### 3. Gmail App Password Setup
1. Enable 2-Factor Authentication on your Gmail account
2. Go to Google Account > Security > 2-Step Verification > App passwords
3. Select "Mail" and "Other (Custom name)" - name it "ATS Resume Tool"
4. Copy the 16-character password (remove spaces)

### 4. Run the Application
```bash
# Terminal 1: Start Backend
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
python run.py

# Terminal 2: Start Frontend
cd frontend/app
npm run dev
```

### 5. Access the Application
- **Frontend:** http://localhost:8080
- **Backend API:** http://localhost:5000
- **Default Admin:** vigneshnaidu022@gmail.com / vignesh123@MBU

## 📦 Dependencies

### Backend Dependencies
All backend dependencies are listed in `backend/requirements.txt`:
- Flask 3.1.1 - Web framework
- Flask-JWT-Extended 4.7.1 - JWT authentication
- Flask-Mail 0.10.0 - Email functionality
- Flask-CORS - Cross-origin resource sharing
- Flask-PyMongo - MongoDB integration
- PyMuPDF - PDF processing
- docx2txt - DOCX processing
- sentence-transformers - AI embeddings
- scikit-learn - Machine learning utilities

### Frontend Dependencies
All frontend dependencies are listed in:
- `frontend/requirements.txt` - Human-readable dependency list
- `frontend/package-requirements.json` - Package.json format for easy installation

**Core Frontend Dependencies:**
- React 18.3.1 - UI framework
- Vite 5.4.1 - Build tool
- Tailwind CSS 3.4.11 - Styling
- shadcn/ui - UI components
- Chart.js 4.5.0 - Data visualization
- Axios 1.10.0 - HTTP client
- React Hook Form 7.53.0 - Form management

**Installation Options:**
```bash
# Option 1: Standard npm install
cd frontend/app
npm install

# Option 2: Using requirements file
cd frontend
npm install --package-lock-only
npm ci

# Option 3: Install specific versions
npm install react@18.3.1 react-dom@18.3.1 vite@5.4.1
```

## 🔌 API Endpoints

### Authentication
- `POST /api/signup/` - User registration
- `POST /api/login/` - User login
- `POST /api/verify-otp/` - OTP verification
- `POST /api/forgot-password/` - Password reset request
- `POST /api/validate-reset-otp/` - Reset OTP validation
- `POST /api/reset-password/` - Password reset

### Resume Management
- `POST /api/upload-resume/` - Upload resume file
- `POST /api/parse-resume/` - Parse resume content

### ATS Scoring
- `POST /api/get-ats-score/` - Get ATS score and analysis

### AI Suggestions
- `POST /api/get-suggestions/` - Get AI-powered improvements

### Admin Functions
- `GET /api/admin/users/` - List all users
- `GET /api/admin/resumes/` - List all resumes
- `DELETE /api/admin/delete-user/{id}` - Delete user
- `GET /api/admin/all-activities/` - Get all activities

### User Activity
- `GET /api/user-activity/` - Get user activity stats

## 🎨 User Interface

### Landing Page
- Modern, responsive design
- Feature highlights
- Call-to-action buttons
- Navigation to login/register

### Authentication Pages
- Clean, modern forms
- Real-time validation
- OTP input with auto-focus
- Password strength indicators

### Dashboard
- Activity overview with charts
- Quick action buttons
- Recent activities list
- Statistics cards

### Resume Upload
- Drag & drop interface
- File validation
- Progress indicators
- Preview functionality

### ATS Scoring
- Interactive charts
- Score breakdown
- Missing keywords display
- Improvement suggestions

### AI Suggestions
- Section-wise improvements
- Copy-to-clipboard buttons
- Interactive keyword suggestions
- Professional tone enhancement

### Admin Dashboard
- User management table
- Resume analytics
- Activity monitoring
- System health indicators

## 🔐 Security Features

### Authentication & Authorization
- **JWT Tokens** with automatic refresh
- **OTP Verification** via email
- **Role-based Access Control** (User/Admin)
- **Password Hashing** with bcrypt
- **Rate Limiting** on sensitive endpoints

### Data Protection
- **CORS Configuration** for cross-origin requests
- **Input Validation** and sanitization
- **Secure File Upload** with validation
- **Environment Variable** protection

### API Security
- **Request Validation** with proper error handling
- **Token-based Authentication** for protected routes
- **CSRF Protection** through JWT tokens
- **Secure Headers** configuration

## 🤖 AI/ML Features

### ATS Scoring Algorithm
- **Local sentence-transformers** for embeddings
- **Cosine similarity** scoring
- **Keyword matching** algorithms
- **Skill relevance** analysis
- **Missing keywords** identification

### Resume Parsing
- **PDF Processing** with PyMuPDF
- **DOCX Processing** with docx2txt
- **Structured Data Extraction**
- **Contact Information** detection
- **Skill and Experience** parsing

### AI Suggestions
- **Context-aware** improvements
- **Section-specific** suggestions
- **Keyword optimization**
- **Professional tone** enhancement
- **Grammar and style** improvements

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

## 🚀 Deployment

### Backend Deployment
```bash
# Production environment variables
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret
MONGO_URI=mongodb://your-production-mongo-uri
CORS_ORIGINS=https://yourdomain.com

# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Serve with nginx or similar
# Copy dist/ contents to web server
```

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]

# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 8080
CMD ["npm", "run", "preview"]
```

## 🧪 Testing

### Backend Testing
```bash
# API testing with curl
curl -X POST http://localhost:5000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"password123"}'

# Unit testing
python -m pytest tests/
```

### Frontend Testing
```bash
# Component testing
npm test

# E2E testing
npm run test:e2e
```

## 📈 Performance Optimization

### Backend Optimization
- **Database indexing** for faster queries
- **Caching** for frequently accessed data
- **Async processing** for heavy operations
- **Connection pooling** for database

### Frontend Optimization
- **Code splitting** with React Router
- **Lazy loading** for components
- **Bundle optimization** with Vite
- **Image optimization** and compression

## 🔧 Configuration

### Development Configuration
```bash
# Backend development
export FLASK_ENV=development
export FLASK_DEBUG=1

# Frontend development
export VITE_APP_ENV=development
```

### Production Configuration
```bash
# Backend production
export FLASK_ENV=production
export FLASK_DEBUG=0

# Frontend production
export VITE_APP_ENV=production
```

## 📞 Support & Troubleshooting

### Common Issues

#### Backend Issues
1. **MongoDB Connection Error**
   - Verify MongoDB is running
   - Check connection string in .env
   - Ensure network connectivity

2. **Email Not Sending**
   - Verify Gmail App Password
   - Check 2FA is enabled
   - Validate email configuration

3. **Import Errors**
   - Activate virtual environment
   - Install all requirements
   - Check Python version compatibility

#### Frontend Issues
1. **API Connection Error**
   - Verify backend server is running
   - Check CORS configuration
   - Validate API base URL

2. **Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version
   - Verify all dependencies

3. **Port Conflicts**
   - Change port in vite.config.ts
   - Check for other running services

### Debugging Tips
- Check browser console for frontend errors
- Monitor backend logs for API issues
- Use Network tab to debug API calls
- Verify environment variables are set correctly

## 📚 Documentation

### Detailed Documentation
- **[Backend README](backend/README.md)** - Complete backend documentation
- **[Frontend README](frontend/app/README.md)** - Complete frontend documentation

### API Documentation
- All endpoints with examples
- Request/response schemas
- Authentication requirements
- Error handling

### Component Documentation
- UI component library
- Custom hooks
- Utility functions
- Styling guidelines

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Standards
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/TypeScript
- Write meaningful commit messages
- Add documentation for new features

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **shadcn/ui** for beautiful UI components
- **Tailwind CSS** for utility-first styling
- **Chart.js** for data visualization
- **sentence-transformers** for AI embeddings
- **Flask** for robust backend framework
- **React** for modern frontend development

## 📞 Contact

For support, questions, or contributions:
- **Email:** vigneshnaidu022@gmail.com
- **GitHub:** [Repository Issues](https://github.com/your-repo/issues)

---

**Built with ❤️ for job seekers worldwide**