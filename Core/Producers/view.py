from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from Core.Producers.service import ProducerService
from logging import getLogger

logger = getLogger(__name__)


class ProducerView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of producer by ID",
        security=[{'BearerAuth': []}],
        responses={
            200: 'Producer list or single producer details',
            404: 'Producer not found'
        }
    )
    def get(self, request, producer_id=None):
        try:
            if producer_id:
                producer = ProducerService.get_producer_by_id(producer_id)
                if producer:
                    return Response(
                        {'id': producer.id, 'name': producer.name},
                        status=status.HTTP_200_OK
                    )
                return Response(
                    {'errors': ['Producer not found']},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                producers = ProducerService.get_all_producers()
                return Response(
                    [{'id': p.id, 'name': p.name} for p in producers],
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Error retrieving producers: {str(e)}")
            return Response(
                {'errors': ['An error occurred while processing the request']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Create a new producer",
        security=[{'BearerAuth': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Name of the producer'
                )
            },
            required=['name']
        ),
        responses={
            201: 'Producer created',
            400: 'Name is required'
        }
    )
    def post(self, request):
        try:
            name = request.data.get('name')
            if not name:
                return Response(
                    {'errors': ['Name is required']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            producer = ProducerService.create_producer(name)
            return Response(
                {'id': producer.id, 'name': producer.name},
                status=status.HTTP_201_CREATED
            )
        except ValueError as ve:
            logger.warning(f"Validation error: {str(ve)}")
            return Response(
                {'errors': [str(ve)]},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating producer: {str(e)}")
            return Response(
                {'errors': ['An error occurred while processing the request']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Update an existing producer",
        security=[{'BearerAuth': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='New name of the producer'
                )
            },
            required=['name']
        ),
        responses={
            200: 'Producer updated',
            404: 'Producer not found',
            400: 'Name is required'
        }
    )
    def put(self, request, producer_id):
        try:
            name = request.data.get('name')
            if not name:
                return Response(
                    {'errors': ['Name is required']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            producer = ProducerService.update_producer(producer_id, name)
            if producer:
                return Response(
                    {'id': producer.id, 'name': producer.name},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'errors': ['Producer not found']},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating producer: {str(e)}")
            return Response(
                {'errors': ['An error occurred while processing the request']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_description="Delete a producer",
        security=[{'BearerAuth': []}],
        responses={
            204: 'Producer deleted',
            404: 'Producer not found'
        }
    )
    def delete(self, request, producer_id):
        try:
            success = ProducerService.delete_producer(producer_id)
            if success:
                return Response(
                    {'message': 'Producer deleted'},
                    status=status.HTTP_204_NO_CONTENT
                )
            return Response(
                {'errors': ['Producer not found']},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting producer: {str(e)}")
            return Response(
                {'errors': ['An error occurred while processing the request']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
