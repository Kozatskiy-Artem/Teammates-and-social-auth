from annoying.functions import get_object_or_None
from django.db.models import QuerySet

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

        product = Person.objects.create(
            first_name=new_person_dto.first_name,
            last_name=new_person_dto.last_name,
            email=new_person_dto.email,
        )

        return self._person_to_dto(product)

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

        person = get_object_or_None(Person, id=person_id)
        if person:
            return self._person_to_dto(person)
        raise InstanceDoesNotExistError(f"Person with id {person_id} not found")

    def update_person(self, person_id: int, person_dto: PersonDTO) -> PersonDTO:
        """
        Update person information

        Args:
            person_id (int): The unique identifier of the person.
            person_dto (PersonDTO): The data model object representing data of a person.

        Returns:
            PersonDTO - A data transfer object containing the person information.

        Raises:
            InstanceDoesNotExistError: If no person with this id is found.
        """

        person = get_object_or_None(Person, id=person_id)

        if not person:
            raise InstanceDoesNotExistError(f"Person with id {person_id} not found")

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

        person = get_object_or_None(Person, id=person_id)

        if not person:
            raise InstanceDoesNotExistError(f"Person with id {person_id} not found")

        person.delete()

    def get_persons(self) -> list[PersonDTO]:
        """
        Retrieve a list of persons filtered by the provided parameters.

        Returns:
            list(PersonDTO) - A list of data transfer objects containing information about persons.

        Raises:
            InstanceDoesNotExistError: If no persons is found.
        """

        persons = Person.objects.all()

        if not persons.exists():
            raise InstanceDoesNotExistError("Persons not found")

        return self._persons_to_dto(persons)

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
            email=person.email
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
