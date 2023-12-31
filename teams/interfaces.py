from abc import ABCMeta, abstractmethod

from .dto import NewTeamDTO, TeamDTO, MemberIdDTO


class TeamRepositoryInterface(metaclass=ABCMeta):
    """
    Interface for team repository.

    This interface defines methods that must be implemented by any class
    acting as a repository for teams data. By adhering to this interface,
    classes ensure consistent behavior for accessing team information
    regardless of their specific implementations.

    By using this interface, you can easily swap out different repository
    implementations without affecting other parts of the application that
    depend on teams.
    """

    @abstractmethod
    def create_team(self, new_team_dto: NewTeamDTO) -> TeamDTO:
        """
        Create a new team

        Args:
            new_team_dto (NewTeamDTO): The data model object representing a team.

        Returns:
            TeamDTO - A data transfer object containing the team information.

        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def update_team(self, team_id: int, team_dto: NewTeamDTO) -> TeamDTO:
        """
        Update team information

        Args:
            team_id (int): The unique identifier of the team.
            team_dto (NewTeamDTO): The data model object representing data of a team.

        Returns:
            TeamDTO - A data transfer object containing the team information.

        Raises:
            InstanceDoesNotExistError: If no team with this id is found.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_teams(self) -> list[TeamDTO]:
        """
        Retrieve a list of teams.

        Returns:
            list(TeamDTO) - A list of data transfer objects containing information about teams.

        Raises:
            InstanceDoesNotExistError: If no teams is found.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass
