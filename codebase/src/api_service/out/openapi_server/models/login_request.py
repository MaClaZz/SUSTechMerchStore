from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class LoginRequest(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, username=None, password=None):  # noqa: E501
        """LoginRequest - a model defined in OpenAPI

        :param username: The username of this LoginRequest.  # noqa: E501
        :type username: str
        :param password: The password of this LoginRequest.  # noqa: E501
        :type password: str
        """
        self.openapi_types = {
            'username': str,
            'password': str
        }

        self.attribute_map = {
            'username': 'username',
            'password': 'password'
        }

        self._username = username
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'LoginRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The LoginRequest of this LoginRequest.  # noqa: E501
        :rtype: LoginRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def username(self) -> str:
        """Gets the username of this LoginRequest.


        :return: The username of this LoginRequest.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this LoginRequest.


        :param username: The username of this LoginRequest.
        :type username: str
        """
        if username is None:
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501

        self._username = username

    @property
    def password(self) -> str:
        """Gets the password of this LoginRequest.


        :return: The password of this LoginRequest.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this LoginRequest.


        :param password: The password of this LoginRequest.
        :type password: str
        """
        if password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501

        self._password = password
