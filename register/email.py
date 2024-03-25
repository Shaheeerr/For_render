from django.core.mail import send_mail
from pyotp import OTP
import pyotp  #import pyotp 


def generate_otp():  # for generate six digit otp
    totp = pyotp.TOTP(pyotp.random_base32(), digits=6)
    return totp.now()

def send_otp_to_email(email, otp): # send the otp function for user email
    subject = 'Your OTP for Registration'
    message = f'Your OTP for registration is: {otp}'
    from_email = 'undeafteadecommerce@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list) #send the mail to the user


