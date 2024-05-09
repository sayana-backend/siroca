from ..application.views import CustomPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .permissions import *
from rest_framework import filters
from .models import CustomUser


class CreateUserView(generics.CreateAPIView):
    '''Create user'''
    queryset = CustomUser.objects.select_related("main_company", "job_title").only("role_type").all()
    serializer_class = UserProfileRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.create_user(**serializer.validated_data)

        '''Set general permissions to new user'''
        first_client = CustomUser.objects.filter(role_type='client').first()
        first_manager = CustomUser.objects.filter(role_type='manager').first()

        if first_client:
            user.client_can_edit_comments = first_client.client_can_edit_comments
            user.client_can_get_reports = first_client.client_can_get_reports
            user.client_can_view_logs = first_client.client_can_view_logs
            user.client_can_add_files = first_client.client_can_add_files
            user.client_can_add_checklist = first_client.client_can_add_checklist
            user.save()

        elif first_manager:
            user.manager_can_delete_comments = first_manager.manager_can_delete_comments
            user.manager_can_get_reports = first_manager.manager_can_get_reports
            user.manager_can_delete_application = first_manager.manager_can_delete_application
            user.save()
        else:
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListUserProfileView(generics.ListAPIView):
    '''list users'''
    queryset = CustomUser.objects.select_related("main_company", "job_title").all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsManagerCanCreateAndEditUserOrIsAdminUser]
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'surname', 'main_company__name']


class DetailUserProfileView(generics.RetrieveDestroyAPIView):
    '''User profile view and delete'''
    queryset = CustomUser.objects.select_related("main_company", "job_title").all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class UserUpdateView(generics.RetrieveUpdateAPIView):
    '''User update'''
    queryset = CustomUser.objects.select_related("main_company", "job_title").all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class ListUserONlyNameView(generics.ListAPIView):
    '''list users for front'''
    queryset = CustomUser.objects.select_related("main_company", "job_title").all()
    serializer_class = UserListOnlyNameSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'surname', 'username', 'full_name']




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
                'id': user.id,
                'role_type': user.role_type,
                'name': user.first_name,
                'refreshToken': str(refresh),
                'access': str(access_token),
                'refresh_lifetime_days': refresh.lifetime.days,
                'access_lifetime_days': access_token.lifetime.days
            })
        else:
            return Response({'detail': 'Ошибка аутентификации'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refreshToken')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'detail': 'Вы успешно вышли'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'detail': 'Ошибка выхода из системы'}, status=status.HTTP_400_BAD_REQUEST)


class AdminContactDetailView(generics.RetrieveUpdateAPIView):
    '''Редактирование контактов админа в профиле админа'''
    serializer_class = AdminContactSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AdminContact.objects.all()
        return AdminContact.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()

        if obj is None:
            return Response({'detail': 'Ошибка аутентификации'}, status=status.HTTP_404_NOT_FOUND)
        return obj


class AdminContactListView(generics.ListAPIView):
    '''Контакты админа при авторизации'''
    queryset = AdminContact.objects.all()
    serializer_class = AdminContactSerializer


class ChangePasswordView(generics.UpdateAPIView):
    '''смена пароля в профиле у каждого пользователя'''
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password1 = serializer.validated_data.get('new_password1')
        new_password2 = serializer.validated_data.get('new_password2')

        if not user.check_password(old_password):
            return Response({'detail': 'Старый пароль неверен'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password1 != new_password2:
            return Response({'detail': 'Новые пароли не совпадают'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password1)
        user.save()

        return Response({'detail': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)


class AdminResetPasswordView(generics.UpdateAPIView):
    '''Сброс пароля админом в случае если пароль забыли'''
    queryset = CustomUser.objects.all()
    serializer_class = AdminResetPasswordSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({'detail': 'Новый пароль и его подтверждение не совпадают.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Пароль пользователя успешно сброшен.', 'new_password': new_password}, status=status.HTTP_200_OK)

