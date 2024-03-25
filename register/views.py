from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
import jwt
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.conf import settings
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse



class RegisterUserView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data) 
        if serializer.is_valid(): # check the serializer is valid
            user = serializer.save()

            verify_user_url = reverse('verify_user') # after the user save change the url into the login

            return Response({
                    "detail": "User created successfully.",
                    "user_details": {
                    "username": user.username,
                    "email": user.email,
                    "otp": user.otp,
                    "verification_link": verify_user_url}}, status=status.HTTP_200_OK)   # return the function to the login url

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   # return the serializer id not valid




class VerifyUserView(APIView):  # otp verify view
    def post(self, request):
        try:
            serializer = OtpSerializer(data=request.data)
            verify_otp_url=reverse('user_login')   # success url 

            if serializer.is_valid():  # check the serializer is valid
                email = serializer.validated_data['email']

                user = CustomUser.objects.get(email=email)  
                user.is_verified = True   # is_verified field set true for login
                user.save()    #save the user

                return Response({
                    "message": "Verified successfully",
                    "user_details": {
                    "login_link": verify_otp_url}
                    }, status=status.HTTP_200_OK)


        except serializers.ValidationError as e:   #exception
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # return error when serilizer is not valid




class Otp_resend(APIView): # resend otp view
    def post(self, request, *args, **kwargs):
        serializer = OtpResendSerializer(data=request.data)
        if serializer.is_valid():  # check the serializer
            email = serializer.validated_data.get('email')

            # Get the user from the database (already validated in the serializer)
            user = CustomUser.objects.get(email=email)

            # Resend OTP using the serializer method
            new_otp = serializer.resend_otp(user)
            

            return Response({'message': 'OTP resent successfully.', 'user': new_otp, 'name': user.username}, status=status.HTTP_200_OK) # return the function
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # return error when serilizer is not valid


            


class UserLoginView(APIView): # login view
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(): # check the serializer is valid or not
            user_data = serializer.validated_data
            return Response(user_data, status=status.HTTP_200_OK) # return the serilizer is valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
























































































































































