import logging
from Core.Movies.service import MovieService
from Core.Winners.serlializer import WinnerSerializer
from Core.Winners.service import WinnerCSVService, WinnerService
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated


logger = logging.getLogger(__name__)


class WinnerView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get all winners.",
        responses={
            200: "List of winners.",
            404: "No winners found."
        }
    )
    def get(self, request, winner_id=None):
        try:
            if winner_id:
                winner = WinnerService.get_winner_by_id(winner_id)
                if winner:
                    return Response(
                        {
                            "winner": f"{winner.award} - {winner.movie.title}"
                        },
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {"error": "Winner not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            winners = WinnerService.get_all_winners()
            if winners:
                winners_list = [
                    {
                        "award": winner.award,
                        "year": winner.year,
                        "movie": winner.movie.title
                    } for winner in winners
                ]
                return Response(
                    {"winners": winners_list},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "No winners found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error retrieving winners: {e}")
            return Response(
                {"error": f"Error retrieving winners: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Create a new award winner.",
        request_body=WinnerSerializer,
        responses={
            201: "Winner created successfully.",
            400: "Input validation error.",
            500: "Internal server error."
        }
    )
    def post(self, request):
        try:
            serializer = WinnerSerializer(data=request.data)
            if serializer.is_valid():
                movie_title = serializer.validated_data['movie']
                producer_data = serializer.validated_data['producer']
                studio_data = serializer.validated_data['studio']
                award = serializer.validated_data['title']
                year = serializer.validated_data['year']

                movie = MovieService.get_or_create_movie(
                    movie_title, producer_data, studio_data
                )
                if not movie:
                    return Response(
                        {"error": "Failed to create or update movie."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                winner = WinnerService.create_winner(
                    award, year, movie
                )
                if winner:
                    return Response(
                        {"message": "Winner created successfully."},
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    {"error": "Failed to create winner."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response(
                {"error": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating winner: {e}")
            return Response(
                {"error": f"Error creating winner: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Update an existing winner.",
        request_body=WinnerSerializer,
        responses={
            200: "Winner updated successfully.",
            400: "Input validation error.",
            404: "Winner not found.",
            500: "Internal server error."
        }
    )
    def put(self, request, winner_id):
        try:
            serializer = WinnerSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            validated_data = serializer.validated_data
            movie_title = validated_data.get('movie')
            producer_data = validated_data.get('producer')
            studio_data = validated_data.get('studio')
            award = validated_data.get('title')
            year = validated_data.get('year')

            if not movie_title or not producer_data or not studio_data:
                return Response(
                    {"error": "Movie, producer, and studio are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            movie = MovieService.get_or_create_movie(
                movie_title, producer_data, studio_data
            )
            if not movie:
                return Response(
                    {"error": "Failed to create or update movie."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            winner = WinnerService.update_winner(
                winner_id, movie.id, award, year
            )
            if not winner:
                return Response(
                    {"error": "Winner not found or failed to update."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {"message": "Winner updated successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error updating winner: {e}")
            return Response(
                {"error": f"Error updating winner: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @swagger_auto_schema(
        operation_description="Delete a winner.",
        responses={
            204: "Winner deleted successfully.",
            404: "Winner not found.",
            500: "Internal server error."
        }
    )
    def delete(self, request, winner_id):
        try:
            success = WinnerService.delete_winner(winner_id)
            if success:
                return Response(
                    {"message": "Winner deleted successfully."},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {"error": "Winner not found or failed to delete."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting winner: {e}")
            return Response(
                {"error": f"Error deleting winner: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WinnerImportCSVView(APIView):
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return JsonResponse(
                {"error": "CSV file not provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        service = WinnerCSVService(csv_file)
        processed_data, data_list_errors = service.process_and_prepare_data(
            csv_file.read().decode('utf-8'), old_delim=', ', new_delim=';'
        )

        if not processed_data:
            return JsonResponse(
                {"error": "Error processing CSV data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        success_count = len(processed_data)

        status_code = status.HTTP_200_OK
        return JsonResponse(
            {
                "success_count": success_count,
                "data_list": str(processed_data),
                "errors": str(data_list_errors)
            }, safe=False, status=status_code)
