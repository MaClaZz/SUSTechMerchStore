from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class OrderRequest(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, product_id=None, quantity=None):  # noqa: E501
        """OrderRequest - a model defined in OpenAPI

        :param product_id: The product_id of this OrderRequest.  # noqa: E501
        :type product_id: int
        :param quantity: The quantity of this OrderRequest.  # noqa: E501
        :type quantity: int
        """
        self.openapi_types = {
            'product_id': int,
            'quantity': int
        }

        self.attribute_map = {
            'product_id': 'productId',
            'quantity': 'quantity'
        }

        self._product_id = product_id
        self._quantity = quantity

    @classmethod
    def from_dict(cls, dikt) -> 'OrderRequest':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The OrderRequest of this OrderRequest.  # noqa: E501
        :rtype: OrderRequest
        """
        return util.deserialize_model(dikt, cls)

    @property
    def product_id(self) -> int:
        """Gets the product_id of this OrderRequest.


        :return: The product_id of this OrderRequest.
        :rtype: int
        """
        return self._product_id

    @product_id.setter
    def product_id(self, product_id: int):
        """Sets the product_id of this OrderRequest.


        :param product_id: The product_id of this OrderRequest.
        :type product_id: int
        """

        self._product_id = product_id

    @property
    def quantity(self) -> int:
        """Gets the quantity of this OrderRequest.


        :return: The quantity of this OrderRequest.
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """Sets the quantity of this OrderRequest.


        :param quantity: The quantity of this OrderRequest.
        :type quantity: int
        """

        self._quantity = quantity
