from abc import ABCMeta, abstractmethod

from .dto import NewTeamDTO, TeamDTO


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
