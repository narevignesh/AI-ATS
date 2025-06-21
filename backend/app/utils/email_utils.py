from flask_mail import Message
from flask import current_app
import random
import os

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(mail, to, otp):
    try:
        print(f"Attempting to send OTP email to: {to}")  # Debug log
        
        # Check if email configuration is properly set
        mail_username = current_app.config.get('MAIL_USERNAME')
        mail_password = current_app.config.get('MAIL_PASSWORD')
        
        if not mail_username or mail_username == 'your_email@gmail.com' or mail_username == 'vigneshnare225@gmail.com':
            print(f"⚠️  EMAIL CONFIGURATION ISSUE: MAIL_USERNAME not set properly")
            print(f"🔧 To fix: Update MAIL_USERNAME in .env file with your actual Gmail address")
            raise Exception("Email username not configured properly. Please update MAIL_USERNAME in .env file")
        
        if not mail_password or mail_password == 'your-app-password-here' or mail_password == 'your-gmail-app-password-here':
            print(f"⚠️  EMAIL CONFIGURATION ISSUE: MAIL_PASSWORD not set properly")
            print(f"🔧 To fix: Set up Gmail App Password in .env file")
            raise Exception("Email password not configured properly. Please set up Gmail App Password in .env file")
        
        print(f"Mail configuration - Username: {mail_username}")  # Debug log
        
        msg = Message('Your OTP Verification Code - ATS Resume Tool',
                      sender=mail_username,
                      recipients=[to])
        msg.body = f'''
Hello!

Your OTP verification code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
ATS Resume Tool Team
        '''
        msg.html = f'''
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #007bff;">ATS Resume Tool</h2>
    <h3>Your OTP Verification Code</h3>
    <p>Hello!</p>
    <p>Your OTP verification code is:</p>
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; margin: 20px 0;">
        <h1 style="color: #007bff; margin: 0; font-size: 32px; letter-spacing: 5px;">{otp}</h1>
    </div>
    <p><strong>This code will expire in 10 minutes.</strong></p>
    <p>If you didn't request this code, please ignore this email.</p>
    <hr>
    <p style="color: #6c757d; font-size: 12px;">Best regards,<br>ATS Resume Tool Team</p>
</div>
        '''
        
        mail.send(msg)
        print(f"✅ OTP email sent successfully to: {to}")  # Debug log
        return True
        
    except Exception as e:
        print(f"❌ Error sending OTP email to {to}: {str(e)}")  # Debug log
        print(f"Error type: {type(e).__name__}")  # Debug log
        
        # If email fails, we can still proceed by creating the user as unverified
        # This allows the system to work even without email configuration
        print(f"ℹ️  Email sending failed, but user can still be created as unverified")
        raise e

def create_env_file():
    """Create a sample .env file if it doesn't exist"""
    env_content = """# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/ATS

# Email Configuration - Update these with your real Gmail credentials
MAIL_USERNAME=your-actual-gmail@gmail.com
MAIL_PASSWORD=your-16-character-gmail-app-password

# CORS Configuration
CORS_ORIGINS=http://localhost:8080,http://localhost:3000

# Optional: Gemini API (if using)
GEMINI_API_KEY=your_gemini_api_key_here
"""
    
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    
    if not os.path.exists(env_path):
        with open(env_path, 'w') as f:
            f.write(env_content)
        print(f"Created .env file at: {env_path}")
        print("Please update the email credentials in the .env file")
    else:
        print(f".env file already exists at: {env_path}") 