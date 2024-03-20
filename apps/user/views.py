from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsManagerCanEdit


class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer


class ListUserProfileView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer


class DetailUserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'

class UserLoginView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserAuthSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'detail': 'Вы успешно вошли',
                'name': user.first_name,
                'refresh-token': str(refresh),
                'access': str(access_token),
                'refresh_lifetime_days': refresh.lifetime.days,
                'access_lifetime_days': access_token.lifetime.days
            })
        else:
            return Response({'detail': 'Ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)

#     template_name = ''
#     success_url = reverse_lazy('')
#     permission_required = 'user.add_userprofile'


class ContactListView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()
        if obj is None:
            obj = Contact.objects.create(user=self.request.user)
        return obj


class ManagerPermissionsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(role_type='manager')
    serializer_class = ManagerPermissionsSerializer
    permission_classes = [IsManagerCanEdit]

    def update(self, request, *args, **kwargs):
        manager_can_edit = request.data.get('manager_can_edit')
        manager_can_get_reports = request.data.get('manager_can_get_reports')
        if manager_can_edit:
            self.queryset.update(manager_can_edit=True)
        if manager_can_get_reports:
            self.queryset.update(manager_can_get_reports=True)
        return Response('Права менеджера предоставлены')

class ClientPermissionsView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(role_type='client')
    serializer_class = ClientPermissionsSerializer
    # lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        client_can_put_comments = request.data.get('client_can_put_comments')
        client_can_get_reports = request.data.get('client_can_get_reports')
        client_can_view_logs = request.data.get('client_can_view_logs')
        client_can_delete_comments = request.data.get('client_can_delete_comments')
        client_can_add_checklist = request.data.get('client_can_add_checklist')
        if client_can_put_comments:
            self.queryset.update(client_can_put_comments=True)
        if client_can_get_reports:
            self.queryset.update(client_can_get_reports=True)
        if client_can_view_logs:
            self.queryset.update(client_can_view_logs=True)
        if client_can_delete_comments:
            self.queryset.update(client_can_delete_comments=True)
        if client_can_add_checklist:
            self.queryset.update(client_can_add_checklist=True)
        return Response('Права клиента предоставлены')



