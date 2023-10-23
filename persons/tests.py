from django.test import TestCase
from annoying.functions import get_object_or_None

from .dto import NewPersonDTO
from .repositories import PersonRepository
from .models import Person
from core.exceptions import InstanceDoesNotExistError
from teams.models import Team


class PersonRepositoryTestCase(TestCase):

    def setUp(self):
        self.repository = PersonRepository()
        person = Person.objects.create(first_name="First", last_name="Person", email="person@gmail.com")
        self.person_id = person.id

    def test_get_person_by_id(self):
        retrieved_person = self.repository.get_person_by_id(self.person_id)
        self.assertEqual(retrieved_person.first_name, "First")

    def test_create_person(self):
        new_person_dto = NewPersonDTO(first_name="John", last_name="Doe", email="john.doe@example.com")
        created_person = self.repository.create_person(new_person_dto)
        self.assertEqual(created_person.first_name, "John")

    def test_update_person(self):
        person_dto = NewPersonDTO(first_name="Updated", last_name="Person", email="person@gmail.com")
        updated_person = self.repository.update_person(self.person_id, person_dto)

        self.assertEqual(updated_person.first_name, "Updated")

    def test_delete_person_by_id(self):
        self.repository.delete_person_by_id(self.person_id)

        with self.assertRaises(Person.DoesNotExist):
            Person.objects.get(id=self.person_id)

    def test_person_does_not_exists(self):
        with self.assertRaises(InstanceDoesNotExistError):
            retrieved_person = self.repository.get_person_by_id(101)

    def test_get_persons(self):
        Person.objects.create(first_name="Second", last_name="Person2", email="person2@gmail.com")

        retrieved_person = self.repository.get_persons()

        self.assertEqual(retrieved_person[0].first_name, "First")
        self.assertEqual(retrieved_person[1].first_name, "Second")
        self.assertEqual(len(retrieved_person), 2)

    def test_get_persons_without_team(self):
        team = Team.objects.create(name="Team name")

        Person.objects.create(first_name="Second", last_name="Person2", email="person2@gmail.com", team=team)

        retrieved_person = self.repository.get_persons(is_without_team=True)

        self.assertEqual(len(retrieved_person), 1)

    def test_leave_team(self):
        team = Team.objects.create(name="Team name")

        person = Person.objects.create(first_name="Second", last_name="Person2", email="person2@gmail.com", team=team)

        self.assertEqual(person.team.id, team.id)

        self.repository.leave_team(person.id)

        person = get_object_or_None(Person, id=person.id)

        self.assertIsNone(person.team)
