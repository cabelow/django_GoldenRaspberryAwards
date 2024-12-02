from rest_framework import serializers
from Core.Movies.service import MovieService
from Core.Studio.repository import StudioRepository


class WinnerSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    year = serializers.IntegerField()
    producer = serializers.CharField(max_length=255)
    studio = serializers.CharField(max_length=255)
    movie = serializers.CharField(max_length=255)

    def validate(self, data):
        """
        Validates and sets the movie and studio fields in the data.
        """
        movie = MovieService.get_or_create_movie(
            data['movie'], data['producer'], data['studio']
        )
        studio = StudioRepository.get_or_create_studio(data['studio'])
        if not movie or not studio:
            raise serializers.ValidationError(
                "Failed to create or retrieve movie or studio"
            )
        data['movie'] = movie
        data['studio'] = studio
        return data


class WinnerCSVSerializer(serializers.Serializer):
    """
    Serializer for processing winner data from a CSV file.
    """
    year = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    studios = serializers.CharField(max_length=255)
    producer = serializers.CharField(max_length=255)
    winner = serializers.CharField(max_length=255)
