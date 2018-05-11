from rest_framework import serializers
from .models import AllCourses,PushMessage

class BuildingCoursesSerializer(serializers.Serializer):
    area = serializers.CharField()
    building = serializers.CharField()
    def validate_data(self, area,building):
        area = data.get('area')
        buiding = data.get('building')
        id_qs = AllCourses.objects.filter(area = area,building = building)
        if not id_qs.exists():
            raise ValidationError("The target is not exist .")
        return data

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllCourses
        fields = '__all__'


class PushMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushMessage
        fields = [
            'author',
            'title',
            'begin_hour',
            'begin_minute',
            'end_hour',
            'end_minute',
            'area',
            'building',
            'room'
        ]