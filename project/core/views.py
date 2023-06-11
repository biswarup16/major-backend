from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from . serializers import *
from django.contrib.auth import authenticate
from . renderers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from . task import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.forms.models import model_to_dict
from django.views import View
from rest_framework.parsers import FormParser, MultiPartParser

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView): 
    renderer_classes = [UserRenderer]   
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        # print(request.data['email'])
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            user = User.objects.get(email=request.data['email'])
            Profile.objects.create(user=user)
            return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email = email, password = password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
                        
        return Response({'msg':'Login Successful'}, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    parser_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password changed successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password reset link sent successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


class CreateRoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    
    def get_queryset(self):
        for row in Room.objects.all().reverse():
            if Room.objects.filter(user=row.user).count() > 1:
                row.delete()
        return Room.objects.all()
    



@api_view()
def DeleteRoomView(request):
    sleepy.delay(20)
    delete_rooms()
    return Response({"message": "Rooms Deleted Successfully"})


class ProfileView(APIView):
    # parser_classes = (MultiPartParser, FormParser)

    def get(self, request, email, format=None):
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.filter(user=user).first()

            if profile:
                user_data = {
                    "user_email": profile.user.email,
                    "skill": profile.skill,
                    "about": profile.about,
                    "address": profile.address,
                    "bio": profile.bio,
                    "language": profile.language,
                    "profile_pic": profile.profile_photo.url,
                    "cover_pic": profile.cover_photo.url,
                    "name": user.name
                }
                return Response(user_data)
            else:
                return Response({"Message": "User Not Found"})
        except Exception as e:
            print(e)
            return Response({"Message": "Error Occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, email, format=None):
        try:
            user = User.objects.get(email=email)
            profile = Profile.objects.filter(user=user).first()

            if profile:
                serializer = ProfileSerializer(profile, data=request.data)
            else:
                serializer = ProfileSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=user)
                return Response({'message': 'Profile updated successfully' if profile else 'Profile created successfully'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"Message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"Message": "Error Occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def dashboard_api(request):
    api = Dashboard.objects.first()
    serialized_data = {
        'demanding_career': api.demanding_career,
        'trending_skill': api.trending_skill,
        'recruiting_companies': api.recruiting_companies,
        # Add more fields as needed
    }
    return JsonResponse(serialized_data, safe=False)

