from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .email import generate_otp, send_otp_to_email    #import function in email.py for generate otp and send email
from rest_framework_simplejwt.tokens import RefreshToken   #import jwt token from rest framework 
import re
from django.utils import timezone
import logging
import datetime


logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):  #inherit modelserializer
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'is_verified', 'otp_time']
        extra_kwargs = {'password': {'write_only': True}}


    def validate_password(self, value): #validate the password above 8 character
        min_length = 8
        if len(value) < min_length:
            raise serializers.ValidationError(f"The password must be at least {min_length} characters long.")
        return value


    def validate_email(self, value): #validate the email
        if not re.match(r"[a-zA-Z0-9._%+-]+@gmail.com$", value):
            raise serializers.ValidationError("The email must be a valid Gmail address.")
        return value


    def create(self, validated_data):  #for create the user
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()   #save the user

        otp = generate_otp()   #for generate the otp
        send_otp_to_email(user.email, otp)   # for send the otp to email
        user.otp = otp
        user.save()          # save the user after otp sending

        logger.info(f" '{user.username}' register successfully with email '{user.email}' at {datetime.datetime.now()}.")

        return user





class OtpSerializer(serializers.Serializer): # otp verification serializer
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):   #validating the data
        email = data.get('email')
        otp = data.get('otp')

        user = CustomUser.objects.filter(email=email).first()   # querying the database to retrieve a CustomUser object based on the provided email

        if not user: # check the user
            raise serializers.ValidationError("Invalid email.")

        print(user.otp)
        print(otp)
        if user.otp != str(otp): # check the otp is correct
            raise serializers.ValidationError("Wrong OTP.")

        return data




        

class OtpResendSerializer(serializers.Serializer):   # resend otp serializer
    email = serializers.EmailField()

    def validate_email(self, value):  
        try:
            user = CustomUser.objects.get(email=value)  #retrive the email
            if user.is_verified:
                raise serializers.ValidationError('User is already verified.')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')

        return value

    
    def generate_otp(self): 
        return generate_otp()   # genarate the otp for resend

    def resend_otp(self, user):   # send the otp and save it
        new_otp = self.generate_otp()

        user.otp = new_otp
        user.otp_creation_time = timezone.now()
        user.save()

        send_otp_to_email(user.email, new_otp)

        return new_otp   #return the new otp





class UserLoginSerializer(serializers.Serializer):   # login serializer
    email = serializers.EmailField(max_length=255, required=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):  
        email = data.get('email')
        password = data.get('password')

               
        # Ensure either username or email is provided
        if not password and not email:          
            raise serializers.ValidationError("Please provide either username or email.")
        

        # Authenticate the user based on username or email and password
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials. Please provide valid username/email and password.") 

        #ensure the the user is verified or not
        if not user.is_verified:
            raise serializers.ValidationError("the user is not otp verified")
       
        refresh = RefreshToken.for_user(user) #generate the token


        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }   # return the refresh and access token





class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        if not value:
            raise serializers.ValidationError("Refresh token not provided")

        try:
            RefreshToken(value).blacklist()
        except Exception as e:
            raise serializers.ValidationError("Error blacklisting refresh token")

        return value







