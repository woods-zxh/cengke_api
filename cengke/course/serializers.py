from rest_framework import serializers
from .models import AllCourses,PushMessage
from account.models import CourseTable
class BuildingCoursesSerializer(serializers.Serializer):
    area = serializers.CharField()
    building = serializers.CharField()
    def validate_data(self, area,building):
        area = data.get('area')
        buiding = data.get('building')
        id_qs = AllCourses.objects.filter(area = area,building = building)
        if not id_qs.exists():
            raise serializers.ValidationError("The target is not exist .")
        return data

class CourseIdSerializer(serializers.Serializer):
    data_id = serializers.CharField()

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllCourses
        fields = '__all__'

class  CourseTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllCourses
        fields = '__all__'

class PushMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushMessage
        fields = '__all__'

        def create(self, validated_data):
            return PushMessage.objects.create(**validated_data)

class SearchSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    start_time = serializers.IntegerField(default=0)
    end_time = serializers.IntegerField(default=0)
    area = serializers.IntegerField(default=0)
    day_in_week=serializers.IntegerField(default=0)

#class RecommendSerializer(serializers.Serializer):
