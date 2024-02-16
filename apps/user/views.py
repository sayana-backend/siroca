from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile, ManagerProfile, AdminProfile
from .serializers import (UserProfileSerializer, UserProfileValidateSerializers,
                          ManagerProfileSerializer, ManagerProfileValidateSerializers,
                          AdminProfileSerializer, AdminProfileValidateSerializer)
from rest_framework.generics import (ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)

class UserListAPIView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'

class ManagerListAPIView(ListCreateAPIView):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer

class ManagerDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ManagerProfile.objects.all()
    serializer_class = ManagerProfileSerializer
    lookup_field = 'id'

class AdminListAPIView(ListCreateAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer

class AdminDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    lookup_field = 'id'
# @api_view(['GET', 'POST'])
# def user_view(request):
#     if request.method == 'GET':
#         director = UserProfile.objects.all()
#         serializer = UserProfileSerializer(director, many=True)
#         return Response(data=serializer.data)
#     else:
#         serializer = UserProfileValidateSerializers(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
#
#         elif request.method == 'POST':
#             name = request.data.get('name')
#             director = UserProfile.objects.create(name=name)
#             serializer = UserProfileSerializer(director)
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#
# @api_view(['GET', 'POST', 'PUT'])
# def userprofile_view(request, id):
#     try:
#         userprofile = UserProfile.objects.get(id=id)
#     except UserProfile.DoesNotExist:
#         return Response(data={'error: User profile not found'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializers = UserProfileSerializer(userprofile)
#         return Response(data=serializers.data)
#     elif request.method == 'POST':
#         serializers = UserProfileValidateSerializers(data=request.data)
#         if not serializers.is_valid():
#             return Response(data={'errors': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PUT':
#         serializers = UserProfileValidateSerializers(data=request.data)
#         if not serializers.is_valid():
#             return Response(data={'errors': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
#         userprofile.first_name = serializers.validated_data.get('first_name')
#         userprofile.last_name = serializers.validated_data.get('last_name')
#         userprofile.username = serializers.validated_data.get('username')
#         userprofile.password = serializers.validated_data.get('password')
#         userprofile.job_title = serializers.validated_data.get('job_title')
#         userprofile.company = serializers.validated_data.get('company')
#         userprofile.groups = serializers.validated_data.get('groups')
#         userprofile.user_permissions_id = serializers.validated_data.get('user_permissions_id')
#         userprofile.save()
#         return Response(data=UserProfileSerializer(userprofile).data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET', 'POST', 'PUT'])
# def managerprofile_view(request, id):
#     try:
#         managerprofile = ManagerProfile.objects.get(id=id)
#     except ManagerProfile.DoesNotExist:
#         return Response(data={'error: Manager profile not found'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializers = ManagerProfileSerializer(managerprofile)
#         return Response(data=serializers.data)
#     elif request.method == 'POST':
#         serializers = ManagerProfileValidateSerializers(data=request.data)
#         if not serializers.is_valid():
#             return Response(data={'errors': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PUT':
#         serializers = ManagerProfileValidateSerializers(data=request.data)
#         if not serializers.is_valid():
#             return Response(data={'errors': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
#         managerprofile.first_name = serializers.validated_data.get('first_name')
#         managerprofile.last_name = serializers.validated_data.get('last_name')
#         managerprofile.username = serializers.validated_data.get('username')
#         managerprofile.password = serializers.validated_data.get('password')
#         managerprofile.job_title_id = serializers.validated_data.get('job_title_id')
#         managerprofile.company_id = serializers.validated_data.get('company_id')
#         managerprofile.groups = serializers.validated_data.get('groups')
#         managerprofile.user_permissions_id = serializers.validated_data.get('user_permissions_id')
#         managerprofile.save()
#         return Response(data=ManagerProfileSerializer(managerprofile).data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET', 'POST', 'PUT'])
# def adminprofile_view(request, id):
#     try:
#         adminprofile = UserProfile.objects.get(id=id)
#     except AdminProfile.DoesNotExist:
#         return Response(data={'error: Admin profile not found'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializers = AdminProfileSerializer(adminprofile)
#         return Response(data=serializers.data)
#     elif request.method == 'POST':
#         serializers = AdminProfileValidateSerializer(data=request.data)
#         if not serializers.is_valid():
#             return Response(data={'errors': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PUT':
#         serializers = AdminProfileValidateSerializer(data=request.data)
#         if not serializers.is_valid():
#             return Response(data={'errors': serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
#         adminprofile.first_name = serializers.validated_data.get('first_name')
#         adminprofile.last_name = serializers.validated_data.get('last_name')
#         adminprofile.username = serializers.validated_data.get('username')
#         adminprofile.password = serializers.validated_data.get('password')
#         adminprofile.job_title_id = serializers.validated_data.get('job_title_id')
#         adminprofile.company_id = serializers.validated_data.get('company_id')
#         adminprofile.groups = serializers.validated_data.get('groups')
#         adminprofile.user_permissions_id = serializers.validated_data.get('user_permissions_id')
#         adminprofile.save()
#         return Response(data=AdminProfileSerializer(adminprofile).data, status=status.HTTP_200_OK)
#
