from rest_framework import serializers
from .models import Producer


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("The name field cannot be empty")
        return value
