from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes

from core.containers import ServiceContainer
from core.exceptions import InstanceDoesNotExistError
from core.serializers import ResponseWithErrorSerializer, ValidationErrorResponseSerializer
from .dto import NewPersonDTO
from .serializers import PersonCreateSerializer, PersonSerializer


class ApiPersonListView(APIView):
    """
    The ApiPersonListView class defines API endpoints for create person and
    working with a list containing information about persons.
    """

    @extend_schema(
        summary="Create a new person",
        request=PersonCreateSerializer,
        responses={
            200: PersonSerializer,
            400: ValidationErrorResponseSerializer
        },
        tags=["Persons"],
    )
    def post(self, request):
        """Handle POST request to create person."""

        person_serializer = PersonCreateSerializer(data=request.data)

        if not person_serializer.is_valid():
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        person_service = ServiceContainer.person_service()

        new_person_dto = NewPersonDTO(**person_serializer.validated_data)

        person_dto = person_service.create_person(new_person_dto)

        person = PersonSerializer(person_dto)

        return Response(
            data=person.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Retrieve information about all persons",
        parameters=[
            OpenApiParameter(
                name="is_without_team",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter products by 'offer of the month' status (True/False).",
            ),
        ],
        responses={
            200: PersonSerializer(many=True),
            404: ResponseWithErrorSerializer,
        },
        tags=["Persons"],
    )
    def get(self, request):
        """Handle GET request to retrieve all persons data."""

        is_without_team = request.query_params.get('is_without_team', None)

        if is_without_team and is_without_team.capitalize() == "True":
            is_without_team = True
        else:
            is_without_team = False

        person_service = ServiceContainer.person_service()

        try:
            persons_dto = person_service.get_persons(is_without_team)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        persons = PersonSerializer(persons_dto, many=True)

        return Response(
            data=persons.data,
            status=status.HTTP_200_OK,
        )


class ApiPersonDetailView(APIView):
    """The ApiPersonDetailView class defines API endpoints for working with person information."""

    @extend_schema(
        summary="Retrieve person data by person id",
        responses={
            200: PersonSerializer,
            404: ResponseWithErrorSerializer,
        },
        tags=["Persons"],
    )
    def get(self, request, id):
        """Handle GET request to retrieve person data."""

        person_service = ServiceContainer.person_service()

        try:
            person_dto = person_service.get_person(id)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        person = PersonSerializer(person_dto)

        return Response(
            data=person.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Delete person data by person id",
        responses={
            204: None,
            404: ResponseWithErrorSerializer,
        },
        tags=["Persons"],
    )
    def delete(self, request, id):
        """Handle DELETE request to remove person data."""

        person_service = ServiceContainer.person_service()

        try:
            person_service.delete_person(id)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        summary="Update person data",
        request=PersonCreateSerializer,
        responses={
            200: PersonSerializer,
            400: ValidationErrorResponseSerializer,
            404: ResponseWithErrorSerializer,
        },
        tags=["Persons"],
    )
    def put(self, request, id):
        """Handle PUT request to update person data."""

        person_serializer = PersonCreateSerializer(data=request.data)

        if not person_serializer.is_valid():
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        person_service = ServiceContainer.person_service()

        update_person_dto = NewPersonDTO(**person_serializer.validated_data)

        try:
            person_dto = person_service.update_person(id, update_person_dto)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        person = PersonSerializer(person_dto)

        return Response(
            data=person.data,
            status=status.HTTP_200_OK,
        )


class ApiLeaveTeamView(APIView):
    """The ApiLeaveTeamView class defines API endpoints for leaving a team."""

    @extend_schema(
        summary="Leave team",
        responses={
            200: PersonSerializer,
            404: ResponseWithErrorSerializer,
        },
        tags=["Persons"],
    )
    def patch(self, request, id):
        """Handle PATCH request for a person to leave the team."""

        person_service = ServiceContainer.person_service()

        try:
            person_dto = person_service.leave_team(id)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        person = PersonSerializer(person_dto)

        return Response(
            data=person.data,
            status=status.HTTP_200_OK,
        )