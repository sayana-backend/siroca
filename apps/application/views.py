from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users
from .serializers import UsersSerializers, UsersValidateSerializers


@api_view(['GET', 'POST'])
def user_view(request):
    if request.method == 'GET':
        user = Users.objects.all().prefetch_related('user')
        serializer = UsersSerializers(user, many=True)
        return Response(data=serializer.data)
    else:
        serializer = UsersValidateSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'errors': serializer.errors})
        elif request.method == 'POST':
            name = request.data.get('name')
            surname = request.data.get('surname')
            login = request.data.get('login')
            password = request.data.get('password')
            position_company_id = request.data.get('position_company_id')
            user_role = request.data.get('user_role')
            create_at = request.data.get('create_at')
            user = Users.objects.create(тame=name, surname=surname, login=login,
                                        password=password,position_company_id=position_company_id,
                                        user_role=user_role, create_at=create_at)
            serializer = UsersSerializers(user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
