from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_otp_email(user_email, otp):
    msg = Message('Verify Your Email - Personal Finance App',
                  recipients=[user_email])
    msg.body = f'''Thank you for registering!
Your OTP for email verification is: {otp}

Please enter this code on the verification page to activate your account.
'''
    print(f"\n[DEBUG] OTP for {user_email}: {otp}\n")
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
