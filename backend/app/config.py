from decouple import config

class Config:
    SECRET_KEY = config('SECRET_KEY', default='your-secret-key-change-this-in-production')
    MONGO_URI = config('MONGO_URI', default='mongodb://localhost:27017/ATS')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='your-jwt-secret-key-change-this-in-production')
    
    # Email Configuration - Using Gmail SMTP
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = config('MAIL_USERNAME', default='vigneshnaidu022@gmail.com')
    MAIL_PASSWORD = config('MAIL_PASSWORD', default='ehfk hnsi ccuc zwlz')
    MAIL_DEFAULT_SENDER = config('MAIL_USERNAME', default='vigneshnaidu022@gmail.com')
    
    # CORS Configuration
    CORS_ORIGINS = config('CORS_ORIGINS', default='http://localhost:8080,http://localhost:3000')
    
    # Optional: Gemini API (if using)
    GEMINI_API_KEY = config('GEMINI_API_KEY', default='AIzaSyCfQd3Q_0eMYAVVC5Ljl2PJSG6y8bI5724') 