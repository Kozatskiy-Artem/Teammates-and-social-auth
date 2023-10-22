from .dto import NewPersonDTO, PersonDTO
from .interfaces import PersonRepositoryInterface


class PersonService:
    """
    The PersonService class is responsible for interacting with the data storage layer,
    specifically the PersonRepository, to retrieve person information.
    """

    def __init__(self, person_repository: PersonRepositoryInterface):
        self.person_repository = person_repository

    def create_person(self, new_person_dto: NewPersonDTO) -> PersonDTO:
        """
        Create a new person

        Args:
            new_person_dto (NewPersonDTO): The data model object representing a person.

        Returns:
            PersonDTO - A data transfer object containing the person information.

        """

        return self.person_repository.create_person(new_person_dto)

    def get_person(self, person_id: int) -> PersonDTO:
        """
        Retrieve information about a person using its unique identifier.

        Args:
            person_id (int): The unique identifier of the person.

        Returns:
            PersonDTO - A data transfer object containing the person information.

        Raises:
            InstanceDoesNotExistError: If no person with this id is found.
        """

        return self.person_repository.get_person_by_id(person_id)

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

        return self.person_repository.update_person(person_id, person_dto)

    def delete_person(self, person_id) -> None:
        """
        Delete information about a person using its unique identifier.

        Args:
            person_id (int): The unique identifier of the person.

        Returns:
            None

        Raises:
            InstanceDoesNotExistError: If no person with this id is found.
        """

        self.person_repository.delete_person_by_id(person_id)

    def get_persons(self, is_without_team: bool = False) -> list[PersonDTO]:
        """
        Retrieve a list of persons, optionally filtered by the absence of a team.

        Returns:
            list(PersonDTO) - A list of data transfer objects containing information about persons.

        Raises:
            InstanceDoesNotExistError: If no persons is found.
        """

        return self.person_repository.get_persons(is_without_team)

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

        return self.person_repository.leave_team(person_id)
