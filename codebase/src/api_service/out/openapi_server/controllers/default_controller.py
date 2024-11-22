import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.get200_response import Get200Response  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server.models.login_response import LoginResponse  # noqa: E501
from openapi_server.models.order import Order  # noqa: E501
from openapi_server.models.order_request import OrderRequest  # noqa: E501
from openapi_server.models.product import Product  # noqa: E501
from openapi_server.models.register_request import RegisterRequest  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.models.user_update import UserUpdate  # noqa: E501
from openapi_server import util


def login_post(login_request):  # noqa: E501
    """Authenticate and get a JWT token

     # noqa: E501

    :param login_request: 
    :type login_request: dict | bytes

    :rtype: Union[LoginResponse, Tuple[LoginResponse, int], Tuple[LoginResponse, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        login_request = LoginRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def orders_order_id_delete(order_id):  # noqa: E501
    """Cancel an order

     # noqa: E501

    :param order_id: 
    :type order_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def orders_order_id_get(order_id):  # noqa: E501
    """Get order details

     # noqa: E501

    :param order_id: 
    :type order_id: int

    :rtype: Union[Order, Tuple[Order, int], Tuple[Order, int, Dict[str, str]]
    """
    return 'do some magic!'


def orders_post(order_request):  # noqa: E501
    """Place a new order

     # noqa: E501

    :param order_request: 
    :type order_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        order_request = OrderRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def products_get():  # noqa: E501
    """List all products

     # noqa: E501


    :rtype: Union[List[Product], Tuple[List[Product], int], Tuple[List[Product], int, Dict[str, str]]
    """
    return 'do some magic!'


def products_product_id_get(product_id):  # noqa: E501
    """Get details of a specific product

     # noqa: E501

    :param product_id: 
    :type product_id: int

    :rtype: Union[Product, Tuple[Product, int], Tuple[Product, int, Dict[str, str]]
    """
    return 'do some magic!'


def register_post(register_request):  # noqa: E501
    """Register a new user

     # noqa: E501

    :param register_request: 
    :type register_request: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        register_request = RegisterRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def root_get():  # noqa: E501
    """Greeting API

    Returns a welcome message at the base URL. # noqa: E501


    :rtype: Union[Get200Response, Tuple[Get200Response, int], Tuple[Get200Response, int, Dict[str, str]]
    """
    return 'do some magic!'


def users_user_id_deactivate_post(user_id):  # noqa: E501
    """Deactivate a user account

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def users_user_id_get(user_id):  # noqa: E501
    """Get user details

     # noqa: E501

    :param user_id: 
    :type user_id: int

    :rtype: Union[User, Tuple[User, int], Tuple[User, int, Dict[str, str]]
    """
    return 'do some magic!'


def users_user_id_put(user_id, user_update):  # noqa: E501
    """Update user information

     # noqa: E501

    :param user_id: 
    :type user_id: int
    :param user_update: 
    :type user_update: dict | bytes

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        user_update = UserUpdate.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
