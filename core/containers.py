from dependency_injector import containers, providers

from persons.repositories import PersonRepository
from persons.services import PersonService


class RepositoryContainer(containers.DeclarativeContainer):
    """
    A container responsible for providing instances of various repository classes.
    Repositories are data access components used by services to retrieve data.
    """

    person_repository = providers.Factory(PersonRepository)


class ServiceContainer(containers.DeclarativeContainer):
    """
    A container responsible for providing instances of various service classes.
    Services are responsible for interaction with the data storage layer and business logic of the application.
    """

    person_service = providers.Factory(PersonService, person_repository=RepositoryContainer.person_repository)
