#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        The method to save the user to the database.
        Args:
            email(str): email
            hashed_password(str): the passwor
        Returns:
            User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Method takes in arbitrary keyword arguments and returns the first row
        found in the users table as filtered by the method’s input arguments
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        The method will use find_user_by to locate the user to update, then
        will update the user’s attributes as passed in the method’s arguments
        then commit changes to the database.
        """
        try:
            user = self.find_user_by(id=user_id)

            for key, val in kwargs.items():
                if not hasattr(user, key):
                    # print(f'user has no {key}')
                    raise ValueError
                setattr(user, key, val)
            self._session.commit()
        except NoResultFound:
            # print('user not found')
            return None
