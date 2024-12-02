from Core.Studio.service import StudioService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class StudioView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of studios or a studio by ID",
        security=[{'BearerAuth': []}],
        responses={
            200: 'Studio list or single studio details',
            404: 'Studio not found'
        }
    )
    def get(self, request, studio_id=None):
        if studio_id:
            studio = StudioService.get_studio_by_id(studio_id)
            if studio:
                return Response(
                    {'id': studio.id, 'name': studio.name},
                    status=status.HTTP_200_OK
                )
            return Response(
                {'errors': ['Studio not found']},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            studios = StudioService.get_all_studios()
            return Response(
                [{'id': s.id, 'name': s.name} for s in studios],
                status=status.HTTP_200_OK
            )

    @swagger_auto_schema(
        operation_description="Create a new studio",
        security=[{'BearerAuth': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Name of the studio'
                )
            },
            required=['name']
        ),
        responses={
            201: 'Studio created',
            400: 'Name is required'
        }
    )
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response(
                {'errors': ['Name is required']},
                status=status.HTTP_400_BAD_REQUEST
            )
        studio = StudioService.create_studio(name)
        return Response(
            {'id': studio.id, 'name': studio.name},
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        operation_description="Update an existing studio",
        security=[{'BearerAuth': []}],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='New name of the studio'
                )
            },
            required=['name']
        ),
        responses={
            200: 'Studio updated',
            404: 'Studio not found',
            400: 'Name is required'
        }
    )
    def put(self, request, studio_id):
        name = request.data.get('name')
        if not name:
            return Response(
                {'errors': ['Name is required']},
                status=status.HTTP_400_BAD_REQUEST
            )
        studio = StudioService.update_studio(studio_id, name)
        if studio:
            return Response(
                {'id': studio.id, 'name': studio.name},
                status=status.HTTP_200_OK
            )
        return Response(
            {'errors': ['Studio not found']},
            status=status.HTTP_404_NOT_FOUND
        )

    @swagger_auto_schema(
        operation_description="Delete a studio",
        security=[{'BearerAuth': []}],
        responses={
            204: 'Studio deleted',
            404: 'Studio not found'
        }
    )
    def delete(self, request, studio_id):
        success = StudioService.delete_studio(studio_id)
        if success:
            return Response(
                {'message': 'Studio deleted'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'errors': ['Studio not found']},
            status=status.HTTP_404_NOT_FOUND
        )
