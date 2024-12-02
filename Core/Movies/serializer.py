from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    producer_name = serializers.SerializerMethodField()
    studio_name = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'winner', 'producer_name', 'studio_name']

    def get_producer_name(self, obj):
        return [producer.name for producer in obj.producer.all()]

    def get_studio_name(self, obj):
        return [studio.name for studio in obj.studio.all()]
