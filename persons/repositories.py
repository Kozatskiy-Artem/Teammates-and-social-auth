from annoying.functions import get_object_or_None
from django.db.models import QuerySet, Q

from core.exceptions import InstanceDoesNotExistError
from .dto import NewPersonDTO, PersonDTO
from .models import Person
from .interfaces import PersonRepositoryInterface


class PersonRepository(PersonRepositoryInterface):
    """The PersonRepository class handles the retrieval of person data from the data storage."""

    def create_person(self, new_person_dto: NewPersonDTO) -> PersonDTO:
        """
        Create a new person

        Args:
            new_person_dto (NewPersonDTO): The data model object representing a person.

        Returns:
            PersonDTO - A data transfer object containing the person information.

        """

        person = Person.objects.create(
            first_name=new_person_dto.first_name,
            last_name=new_person_dto.last_name,
            email=new_person_dto.email,
        )

        return self._person_to_dto(person)

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

        person = self._get_person(person_id)

        return self._person_to_dto(person)

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

        person = self._get_person(person_id)

        person.first_name = person_dto.first_name
        person.last_name = person_dto.last_name
        person.email = person_dto.email

        person.save()

        return self._person_to_dto(person)

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

        person = self._get_person(person_id)

        person.delete()

    def get_persons(self, is_without_team: bool = False) -> list[PersonDTO]:
        """
        Retrieve a list of persons, optionally filtered by the absence of a team.

        Returns:
            list(PersonDTO) - A list of data transfer objects containing information about persons.

        Raises:
            InstanceDoesNotExistError: If no persons is found.
        """

        filter_conditions = Q()

        if is_without_team is True:
            filter_conditions &= Q(team=None)

        persons = Person.objects.filter(filter_conditions)

        if not persons.exists():
            raise InstanceDoesNotExistError("Persons not found")

        return self._persons_to_dto(persons)

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

        person = self._get_person(person_id)

        person.team = None
        person.save()

        return self._person_to_dto(person)

    @staticmethod
    def _person_to_dto(person: Person) -> PersonDTO:
        """
        Convert a data model object (Person) into a PersonDTO object.

        Args:
            person (Person): An instance of the Person model class.

        Returns:
            PersonDTO - A data transfer object containing the person information.
        """

        return PersonDTO(
            id=person.pk,
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            team=person.team
        )

    @classmethod
    def _persons_to_dto(cls, persons: QuerySet[Person]) -> list[PersonDTO]:
        """
        Converts a QuerySet of Person objects to a list of PersonDTO objects.

        Args:
            persons (QuerySet[Person]): A QuerySet of Person objects to be converted.

        Returns:
            list[PersonDTO]: A list of PersonDTO objects containing the converted data.
        """

        persons_dto = [cls._person_to_dto(person) for person in persons]

        return persons_dto

    def _get_person(self, person_id: int) -> Person:
        """
        Retrieve information about a person using its unique identifier.

        Args:
            person_id (int): The unique identifier of the person.

        Returns:
            Person - A person model object containing the person information.

        Raises:
            InstanceDoesNotExistError: If no person with this id is found.
        """

        person = get_object_or_None(Person, id=person_id)

        if not person:
            raise InstanceDoesNotExistError(f"Person with id {person_id} not found")

        return person
