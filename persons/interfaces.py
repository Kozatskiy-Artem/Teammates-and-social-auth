from abc import ABCMeta, abstractmethod

from .dto import NewPersonDTO, PersonDTO


class PersonRepositoryInterface(metaclass=ABCMeta):
    """
    Interface for person repository.

    This interface defines methods that must be implemented by any class
    acting as a repository for persons data. By adhering to this interface,
    classes ensure consistent behavior for accessing person information
    regardless of their specific implementations.

    By using this interface, you can easily swap out different repository
    implementations without affecting other parts of the application that
    depend on persons.
    """

    @abstractmethod
    def create_person(self, new_person_dto: NewPersonDTO) -> PersonDTO:
        """
        Create a new person

        Args:
            new_person_dto (NewPersonDTO): The data model object representing a person.

        Returns:
            PersonDTO - A data transfer object containing the person information.

        """
        pass

    @abstractmethod
    def get_person_by_id(self, person_id: int) -> PersonDTO:
        """
        Retrieve information about a person using its unique identifier.

        Args:
            person_id (int): The unique identifier of the person.

        Returns:
            PersonDTO - A data transfer object containing the person information.

        Raises:
            InstanceDoesNotExistError: If no person with this id is found.
        """
        pass

    @abstractmethod
    def update_person(self, person_id: int, person_dto: NewPersonDTO) -> PersonDTO:
        """
        Update person information

        Args:
            person_id (int): The unique identifier of the person.
            person_dto (NewPersonDTO): The data model object representing data of a person.

        Returns:
            PersonDTO - A data transfer object containing the person information.

        Raises:
            InstanceDoesNotExistError: If no person with this id is found.
        """
        pass

    @abstractmethod
    def delete_person_by_id(self, person_id: int) -> None:
        """
        Delete information about a person using its unique identifier.

        Args:
            person_id (int): The unique identifier of the person.

        Returns:
            None

        Raises:
            InstanceDoesNotExistError: If no person with this id is found.
        """
        pass

    @abstractmethod
    def get_persons(self, is_without_team: bool = False) -> list[PersonDTO]:
        """
        Retrieve a list of persons, optionally filtered by the absence of a team.

        Returns:
            list(PersonDTO) - A list of data transfer objects containing information about persons.

        Raises:
            InstanceDoesNotExistError: If no persons is found.
        """
        pass

    @abstractmethod
    def leave_team(self, person_id: id) -> PersonDTO:
        """
        Remove a person from their team.

        Args:
            person_id (int): The ID of the person.

        Returns:
            PersonDTO - The data transfer object representing the updated person.

        Raises:
            InstanceDoesNotExistError: If the person with the specified ID does not exist.
        """
        pass
