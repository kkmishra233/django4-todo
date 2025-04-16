from django.http import request
from rest_framework import serializers

from app.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ['owner', 'create_date', 'update_date']