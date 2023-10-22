from annoying.functions import get_object_or_None
from django.db.models import QuerySet

from core.exceptions import InstanceDoesNotExistError
from persons.models import Person
from .dto import NewTeamDTO, TeamDTO, MemberIdDTO
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

        team = self._get_team(team_id)

        return self._team_to_dto(team)

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

        team = self._get_team(team_id)

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

        team = self._get_team(team_id)

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

    def add_member(self, team_id: int, new_member_dto: MemberIdDTO) -> TeamDTO:
        """
        Adds a new member to the specified team.

        Args:
            team_id (int): The ID of the team to which the member will be added.
            new_member_dto (MemberIdDTO): Data transfer object representing the new member.

        Returns:
            TeamDTO - An instance of the data transfer object representing the updated team.

        Raises:
            InstanceDoesNotExistError: If the team with the specified ID or the member with the provided ID does not exist.
        """

        team = self._get_team(team_id)

        member = get_object_or_None(Person, id=new_member_dto.id)
        if not member:
            raise InstanceDoesNotExistError(f"Person with id {team_id} not found")

        team.members.add(member)
        team.save()

        return self._team_to_dto(team)

    def remove_member(self, team_id: int, member_dto: MemberIdDTO) -> TeamDTO:
        """
        Adds a new member to the specified team.

        Args:
            team_id (int): The ID of the team to which the member will be added.
            member_dto (MemberIdDTO): Data transfer object representing the member id.

        Returns:
            TeamDTO - An instance of the data transfer object representing the updated team.

        Raises:
            InstanceDoesNotExistError: If the team with the specified ID
             or the member with the provided ID does not exist.
        """

        team = self._get_team(team_id)

        member = get_object_or_None(Person, id=member_dto.id)

        if not member:
            raise InstanceDoesNotExistError(f"Person with id {team_id} not found")

        if member not in team.members.all():
            raise InstanceDoesNotExistError(f"Person with an id {team_id} is not a team member")

        team.members.remove(member)
        team.save()

        return self._team_to_dto(team)

    @staticmethod
    def _team_to_dto(team: Team) -> TeamDTO:
        """
        Convert a data model object (Team) into a TeamDTO object.

        Args:
            team (Team): An instance of the Team model class.

        Returns:
            TeamDTO - A data transfer object containing the team information.
        """

        return TeamDTO(id=team.pk, name=team.name, members=team.members)

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

    def _get_team(self, team_id: int) -> Team:
        """
        Retrieve information about a team using its unique identifier.

        Args:
            team_id (int): The unique identifier of the team.

        Returns:
            Team - A team model object containing the team information.

        Raises:
            InstanceDoesNotExistError: If no team with this id is found.
        """

        team = get_object_or_None(Team, id=team_id)

        if not team:
            raise InstanceDoesNotExistError(f"Team with id {team_id} not found")

        return team
