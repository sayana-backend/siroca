from apps.application.models import ApplicationForm, TrackingPriority, TrackingStatus
from rest_framework import serializers


class TrackingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingStatus
        fields = ('status', 'date_status')


class TrackingPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingPriority
        fields = ('priority', 'date_priority')


class ApplicationFormFilterSerializer(serializers.ModelSerializer):
    status_info = TrackingStatusSerializer(source='trackingstatus_set', many=True, read_only=True)
    priority_info = TrackingPrioritySerializer(source='trackingpriority_set', many=True, read_only=True)
    main_client = serializers.SerializerMethodField()
    main_manager = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationForm
        fields = (
            'task_number', 'title', 'main_client', 'main_manager',
            'application_date', 'start_date', 'finish_date', 'status_info', 'priority_info',
        )

    def get_main_client(self, obj):
        return obj.main_client.first_name if obj.main_client else None

    def get_main_manager(self, obj):
        return obj.main_manager.first_name if obj.main_manager else None
