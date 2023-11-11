import random
from django.core.mail import EmailMessage
from source.auth_service.models import User,OneTimePasswordUser
from config import settings

def generateOTP():
    otp=''
    for i in range(6):
        otp+=str(random.randint(1,9))
    return otp


def send_code_to_user(email):
    Subject='One time Password for User email verification'
    otp_code = generateOTP()
    print(otp_code)
    user =  User.objects.get(email=email)
    current_website = 'auth_service.com'
    email_body_message = f'Hello {user.first_name} {user.last_name} thanks for registration on {current_website},please verify your email with this passcode {otp_code}'
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePasswordUser.objects.create(user=user,code=otp_code)

    d_email = EmailMessage(subject=Subject,body=email_body_message,from_email=from_email,to=[email])
    d_email.send(fail_silently=True,)


def send_resetPasswordLink_to_user(data):
    email = EmailMessage( 
        subject=data['email_subject'],
        body = data['email_body'],
        from_email=settings.EMAIL_HOST,
        to=[data['to_email']])
    email.send(data)
