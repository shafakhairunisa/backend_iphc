import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

OTP_STORAGE = {}

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email: str, otp: str) -> bool:
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        sender_email = os.getenv("GMAIL_EMAIL")
        sender_password = os.getenv("GMAIL_APP_PASSWORD")
        
        print(f"DEBUG: Email config - sender: {sender_email}, has_password: {bool(sender_password)}")
        
        if not sender_email or not sender_password:
            print("DEBUG: Missing email credentials")
            return False
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Reset Password OTP - IPHO Symptom Checker"
        message["From"] = sender_email
        message["To"] = email
        
        html = f"""
        <html>
            <body>
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #2F67E8;">Reset Password OTP</h2>
                    <p>You have requested a password reset for your IPHO Symptom Checker account.</p>
                    <div style="background-color: #f0f0f0; padding: 20px; text-align: center; margin: 20px 0;">
                        <h3 style="color: #2c3e50; font-size: 28px; letter-spacing: 5px; margin: 0;">
                            {otp}
                        </h3>
                    </div>
                    <p>This OTP code is valid for 10 minutes.</p>
                    <p style="color: #666; font-size: 14px;">
                        If you did not request this, please ignore this email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        part = MIMEText(html, "html")
        message.attach(part)
        
        print(f"DEBUG: Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        
        print(f"DEBUG: Email sent successfully to {email}")
        
        # Store OTP
        OTP_STORAGE[email] = {
            "otp": otp,
            "expires_at": datetime.now() + timedelta(minutes=10)
        }
        
        return True
    except Exception as e:
        print(f"DEBUG: Error sending email: {str(e)}")
        return False

def verify_otp(email: str, provided_otp: str) -> bool:
    if email not in OTP_STORAGE:
        return False
    
    stored = OTP_STORAGE[email]
    
    if datetime.now() > stored["expires_at"]:
        del OTP_STORAGE[email]
        return False
    
    if stored["otp"] == provided_otp:
        del OTP_STORAGE[email]
        return True
    
    return False

def cleanup_expired_otps():
    current_time = datetime.now()
    expired_emails = [email for email, data in OTP_STORAGE.items() 
                     if current_time > data["expires_at"]]
    
    for email in expired_emails:
        del OTP_STORAGE[email]