from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from core.containers import ServiceContainer
from core.exceptions import InstanceDoesNotExistError
from core.responses import ResponseWithErrorSerializer, ValidationErrorResponseSerializer
from .dto import NewTeamDTO
from .serializers import TeamCreateSerializer, TeamSerializer


class ApiTeamListView(APIView):
    """
    The ApiTeamListView class defines API endpoints for create team and
    working with a list containing information about teams.
    """

    @extend_schema(
        summary="Create a new team",
        request=TeamCreateSerializer,
        responses={
            200: TeamSerializer,
            400: ValidationErrorResponseSerializer
        },
        tags=["Teams"],
    )
    def post(self, request):
        """Handle POST request to create team."""

        team_serializer = TeamCreateSerializer(data=request.data)

        if not team_serializer.is_valid():
            return Response(team_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        team_service = ServiceContainer.team_service()

        new_team_dto = NewTeamDTO(**team_serializer.validated_data)

        team_dto = team_service.create_team(new_team_dto)

        team = TeamSerializer(team_dto)

        return Response(
            data=team.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Retrieve information about all teams",
        responses={
            200: TeamSerializer(many=True),
            404: ResponseWithErrorSerializer,
        },
        tags=["Teams"],
    )
    def get(self, request):
        """Handle GET request to retrieve all teams data."""

        team_service = ServiceContainer.team_service()

        try:
            teams_dto = team_service.get_teams()
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        teams = TeamSerializer(teams_dto, many=True)

        return Response(
            data=teams.data,
            status=status.HTTP_200_OK,
        )


class ApiTeamDetailView(APIView):
    """The ApiTeamDetailView class defines API endpoints for working with team information."""

    @extend_schema(
        summary="Retrieve team data by team id",
        responses={
            200: TeamSerializer,
            404: ResponseWithErrorSerializer,
        },
        tags=["Teams"],
    )
    def get(self, request, id):
        """Handle GET request to retrieve team data."""

        team_service = ServiceContainer.team_service()

        try:
            team_dto = team_service.get_team(id)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        team = TeamSerializer(team_dto)

        return Response(
            data=team.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Delete team data by team id",
        responses={
            204: None,
            404: ResponseWithErrorSerializer,
        },
        tags=["Teams"],
    )
    def delete(self, request, id):
        """Handle DELETE request to remove team data."""

        team_service = ServiceContainer.team_service()

        try:
            team_service.delete_team(id)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        summary="Update team data",
        request=TeamCreateSerializer,
        responses={
            200: TeamSerializer,
            400: ValidationErrorResponseSerializer,
            404: ResponseWithErrorSerializer,
        },
        tags=["Teams"],
    )
    def put(self, request, id):
        """Handle PUT request to update team data."""

        team_serializer = TeamCreateSerializer(data=request.data)

        if not team_serializer.is_valid():
            return Response(team_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        team_service = ServiceContainer.team_service()

        update_team_dto = NewTeamDTO(**team_serializer.validated_data)

        try:
            team_dto = team_service.update_team(id, update_team_dto)
        except InstanceDoesNotExistError as exception:
            return Response({"error": str(exception)}, status=status.HTTP_404_NOT_FOUND)

        team = TeamSerializer(team_dto)

        return Response(
            data=team.data,
            status=status.HTTP_200_OK,
        )
