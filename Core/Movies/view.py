from xml.dom import ValidationErr
from Core.Movies.models import Movie
from Core.Producers.repository import ProducerRepository
from Core.Studio.repository import StudioRepository
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from Core.Movies.service import ImportMovieCSVService, MovieService
from Core.Movies.serializer import MovieSerializer
import logging
logger = logging.getLogger(__name__)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Core.Movies.service import MovieService
import logging

logger = logging.getLogger(__name__)

class MoviesView(APIView):
    @swagger_auto_schema(
        operation_description="Get all movies or a specific movie.",
        responses={
            200: "List of movies or details of a specific movie.",
            404: "Movie not found."
        }
    )
    def get(self, request, movie_id=None):
        if movie_id:
            try:
                movie = MovieService.get_movie_by_id(movie_id)
                if movie:
                    serialized_movie = MovieSerializer(movie).data
                    return Response({"movie": serialized_movie}, status=status.HTTP_200_OK)
                return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Error fetching movie with ID {movie_id}: {e}")
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        filters = {k: v for k, v in request.query_params.items()}
        try:
            print("filters", filters)
            my_return = MovieService.get_all_movies(filters=filters)
            
            if my_return and my_return['content']:
                return Response(my_return, status=status.HTTP_200_OK)
            return Response({"message": "No movies found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as ve:
            logger.warning(f"Invalid filter value: {ve}")
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    @swagger_auto_schema(
        operation_description="Create a new movie.",
        request_body=MovieSerializer,
        responses={
            201: "Movie created successfully.",
            400: "Input validation error.",
            500: "Internal server error."
        }
    )
    def post(self, request):
        data = request.data
        title = data.get("title")
        year = data.get("year")
        winner = data.get("winner")
        producer_data = data.get("producer")
        studio_data = data.get("studio")
        if not title or not producer_data or not studio_data:
            return Response(
                {"error": "Title, producer, and studio are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        movie = MovieService.create_movie(title, year, producer_data, studio_data, winner)
        if movie:
            return Response(
                {"message": "Movie created successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": "Failed to create movie."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @swagger_auto_schema(
        operation_description="Update an existing movie.",
        request_body=MovieSerializer,
        responses={
            200: "Movie updated successfully.",
            400: "Input validation error.",
            404: "Movie not found.",
            500: "Internal server error."
        }
    )
    def put(self, request, movie_id):
        data = request.data
        title = data.get("title")
        year = data.get("year")
        producer_data = data.get("producer")
        studio_data = data.get("studio")
        winner = data.get("winner")

        if not title or not producer_data or not studio_data:
            return Response(
                {"error": "Title, producer, and studio are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            movie = Movie.objects.get(pk=movie_id)
            movie.title = title
            movie.year = year
            movie.winner = winner
            producers = [
                ProducerRepository.get_or_create_producer([producer['name'].strip()])[0]
                for producer in producer_data if 'name' in producer
            ]
            studios = [
                StudioRepository.get_or_create_studio({'name': studio['name'].strip()})
                for studio in studio_data if 'name' in studio
            ]
            movie.producer.set(producers)
            movie.studio.set(studios)
            movie.save()
            return Response(
                {"message": "Movie updated successfully."},
                status=status.HTTP_200_OK
            )
        except Movie.DoesNotExist:
            return Response(
                {"error": "Movie not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating movie '{title}': {e}")
            return Response(
                {"error": "Failed to update movie."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Delete a movie.",
        responses={
            204: "Movie deleted successfully.",
            404: "Movie not found.",
            500: "Internal server error."
        }
    )
    def delete(self, request, movie_id):
        try:
            success = MovieService.delete_movie(movie_id)
            if success:
                return Response({"message": "Movie deleted successfully."},
                                status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Movie not found or failed to delete."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Error deleting movie: {e}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImportMovieCSVView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = ImportMovieCSVService.process_file(file)
            return Response({
                "message": "File processed successfully.",
                "accepted": result["accepted"],
                "errors": result["errors"]
            }, status=status.HTTP_200_OK)
        except ValidationErr as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class YearsWithMultipleWinnersView(APIView):
    @swagger_auto_schema(
        operation_description="Get years with multiple winners and their counts.",
        responses={
            200: "List of years with the number of times winners appeared in each year."
        }
    )
    def get(self, request):
        try:
            years_with_multiple_winners = MovieService.get_years_with_multiple_winners()
            return Response({"years": years_with_multiple_winners}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in YearsWithMultipleWinnersView: {e}")
            return Response({"error": "An error occurred while fetching the data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudiosWithWinnersView(APIView):
    @swagger_auto_schema(
        operation_description="Get studios with the most wins and their victory counts.",
        responses={
            200: "List of studios with the number of wins they have."
        }
    )
    def get(self, request):
        try:
            studios_with_most_wins = MovieService.get_studios_with_winners()
            return Response({"studios": studios_with_most_wins}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in StudiosWithWinnersView: {e}")
            return Response({"error": "An error occurred while fetching the data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProducersWithWinnerView(APIView):
    @swagger_auto_schema(
        operation_description="Get producers with the largest and smallest intervals between winning movies.",
        responses={
            200: "List of producers with their intervals between winning movies.",
            500: "Internal Server Error when fetching data."
        }
    )
    def get(self, request):
        try:
            producers_with_intervals = MovieService.get_producers_with_winner_intervals()
            if producers_with_intervals:
                return Response(producers_with_intervals, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No data available."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error fetching producers with winner intervals: {e}")
            return Response({"error": "An error occurred while fetching the data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class YearWithWinnerView(APIView):
    @swagger_auto_schema(
        operation_description="Get movies filtered by year and winner status.",
        responses={
            200: "List of movies matching the year and winner filters.",
            404: "No movies found matching the criteria."
        }
    )
    def get(self, request):
        filters = {k: v for k, v in request.query_params.items()}
        try:
            movies = MovieService.get_movies_with_winner(filters=filters)
            if movies:
                return Response({"movies": movies}, status=status.HTTP_200_OK)
            return Response({"message": "No movies found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
