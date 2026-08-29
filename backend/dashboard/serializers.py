from rest_framework import serializers


class DashboardSerializer(serializers.Serializer):

    user = serializers.DictField()

    total_courses = serializers.IntegerField()

    completed_courses = serializers.IntegerField()

    in_progress_courses = serializers.IntegerField()

    total_lessons = serializers.IntegerField()

    completed_lessons = serializers.IntegerField()

    overall_progress = serializers.IntegerField()

    continue_learning = serializers.ListField()