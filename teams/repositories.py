from annoying.functions import get_object_or_None
from django.db.models import QuerySet

from core.exceptions import InstanceDoesNotExistError
from .dto import NewTeamDTO, TeamDTO
from .models import Team
from .interfaces import TeamRepositoryInterface


class TeamRepository(TeamRepositoryInterface):
    """The TeamRepository class handles the retrieval of team data from the data storage."""

    def create_team(self, new_team_dto: NewTeamDTO) -> TeamDTO:
        """
        Create a new team

        Args:
            new_team_dto (NewTeamDTO): The data model object representing a team.

        Returns:
            TeamDTO - A data transfer object containing the team information.
        """

        team = Team.objects.create(name=new_team_dto.name,)

        return self._team_to_dto(team)

    def get_team_by_id(self, team_id: int) -> TeamDTO:
        """
        Retrieve information about a team using its unique identifier.

        Args:
            team_id (int): The unique identifier of the team.

        Returns:
            TeamDTO - A data transfer object containing the team information.

        Raises:
            InstanceDoesNotExistError: If no team with this id is found.
        """

        team = get_object_or_None(Team, id=team_id)
        if team:
            return self._team_to_dto(team)
        raise InstanceDoesNotExistError(f"Team with id {team_id} not found")

    def update_team(self, team_id: int, team_dto: NewTeamDTO) -> TeamDTO:
        """
        Update team information

        Args:
            team_id (int): The unique identifier of the team.
            team_dto (NewTeamDTO): The data model object representing data of a team.

        Returns:
            PersonDTO - A data transfer object containing the team information.

        Raises:
            InstanceDoesNotExistError: If no team with this id is found.
        """

        team = get_object_or_None(Team, id=team_id)

        if not team:
            raise InstanceDoesNotExistError(f"Team with id {team_id} not found")

        team.name = team_dto.name

        team.save()

        return self._team_to_dto(team)

    def delete_team_by_id(self, team_id: int) -> None:
        """
        Delete information about a team using its unique identifier.

        Args:
            team_id (int): The unique identifier of the team.

        Returns:
            None

        Raises:
            InstanceDoesNotExistError: If no team with this id is found.
        """

        team = get_object_or_None(Team, id=team_id)

        if not team:
            raise InstanceDoesNotExistError(f"Team with id {team_id} not found")

        team.delete()

    def get_teams(self) -> list[TeamDTO]:
        """
        Retrieve a list of teams.

        Returns:
            list(TeamDTO) - A list of data transfer objects containing information about teams.

        Raises:
            InstanceDoesNotExistError: If no teams is found.
        """

        teams = Team.objects.all()

        if not teams.exists():
            raise InstanceDoesNotExistError("Teams not found")

        return self._teams_to_dto(teams)

    @staticmethod
    def _team_to_dto(team: Team) -> TeamDTO:
        """
        Convert a data model object (Team) into a TeamDTO object.

        Args:
            team (Team): An instance of the Team model class.

        Returns:
            TeamDTO - A data transfer object containing the team information.
        """

        return TeamDTO(id=team.pk, name=team.name)

    @classmethod
    def _teams_to_dto(cls, teams: QuerySet[Team]) -> list[TeamDTO]:
        """
        Converts a QuerySet of Team objects to a list of TeamDTO objects.

        Args:
            teams (QuerySet[Team]): A QuerySet of Team objects to be converted.

        Returns:
            list[TeamDTO]: A list of TeamDTO objects containing the converted data.
        """

        teams_dto = [cls._team_to_dto(team) for team in teams]

        return teams_dto
