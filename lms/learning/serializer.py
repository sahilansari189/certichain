from rest_framework import serializers
from course.models import Lesson, models
from .models import LessionTracking, ModuleTracking
from course.serializer import ModuleSerializer

class ProgreeSerializer(serializers.ModelSerializer):
    lesson_id = ModuleSerializer()
    completed = serializers.BooleanField()
