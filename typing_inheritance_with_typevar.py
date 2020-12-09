import uuid
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from typing import TypeVar


# Base Repository ###########################################


class IRepository(metaclass=ABCMeta):
    @classmethod
    def info(cls):
        return {"name": cls.__name__}

    @abstractmethod
    def save(self, Any):
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, Any):
        raise NotImplementedError


# User Specific Repository ####################################


@dataclass
class User:
    user_id: str
    name: str


class IUserRepository(IRepository, metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, user_id: str) -> User:
        raise NotImplementedError


# In Memory implementation of User Specific Repository #########
class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self.users = {}

    def save(self, user: User):
        if user.user_id in self.users:
            raise FileExistsError()
        self.users[user.user_id] = user

    def retrieve(self, user_id: str) -> User:
        if user_id not in self.users:
            raise FileNotFoundError()
        return self.users.get(user_id)


def create_random_user(repository: IUserRepository):
    user = User(user_id=str(uuid.uuid4()), name="Davila")
    repository.save(user)


def inheritors(klass):
    subclasses = []
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.append(child)
                work.append(child)
    return tuple(subclasses)


declared_repositories = inheritors(IRepository)

Repository = TypeVar("Repository", IRepository, *declared_repositories)


def repository_provider(name: str) -> Repository:
    if name == "user":
        return InMemoryUserRepository()
    else:
        raise FileNotFoundError()


repository = repository_provider("user")
create_random_user(repository)
