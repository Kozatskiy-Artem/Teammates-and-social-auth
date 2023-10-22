from .dto import NewTeamDTO, TeamDTO, MemberIdDTO
from .interfaces import TeamRepositoryInterface


class TeamService:
    """
    The TeamService class is responsible for interacting with the data storage layer,
    specifically the TeamRepository, to retrieve team information.
    """

    def __init__(self, team_repository: TeamRepositoryInterface):
        self.team_repository = team_repository

    def create_team(self, new_team_dto: NewTeamDTO) -> TeamDTO:
        """
        Create a new team

        Args:
            new_team_dto (NewTeamDTO): The data model object representing a team.

        Returns:
            TeamDTO - A data transfer object containing the team information.
        """

        return self.team_repository.create_team(new_team_dto)

    def get_team(self, team_id: int) -> TeamDTO:
        """
        Retrieve information about a team using its unique identifier.

        Args:
            team_id (int): The unique identifier of the team.

        Returns:
            TeamDTO - A data transfer object containing the team information.

        Raises:
            InstanceDoesNotExistError: If no team with this id is found.
        """

        return self.team_repository.get_team_by_id(team_id)

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

        return self.team_repository.update_team(team_id, team_dto)

    def delete_team(self, team_id) -> None:
        """
        Delete information about a team using its unique identifier.

        Args:
            team_id (int): The unique identifier of the team.

        Returns:
            None

        Raises:
            InstanceDoesNotExistError: If no team with this id is found.
        """

        self.team_repository.delete_team_by_id(team_id)

    def get_teams(self) -> list[TeamDTO]:
        """
        Retrieve a list of teams.

        Returns:
            list(TeamDTO) - A list of data transfer objects containing information about teams.

        Raises:
            InstanceDoesNotExistError: If no teams is found.
        """

        return self.team_repository.get_teams()

    def add_member(self, team_id: int, new_member_dto: MemberIdDTO) -> TeamDTO:
        """
        Adds a new member to the specified team.

        Args:
            team_id (int): The ID of the team to which the member will be added.
            new_member_dto (MemberIdDTO): Data transfer object representing the new member.

        Returns:
            TeamDTO - An instance of the data transfer object representing the updated team.

        Raises:
            InstanceDoesNotExistError: If the team with the specified ID or
             the member with the provided ID does not exist.
        """

        return self.team_repository.add_member(team_id, new_member_dto)

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

        return self.team_repository.remove_member(team_id, member_dto)