# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: db_service.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'db_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x64\x62_service.proto\x12\tdbservice\"\x07\n\x05\x45mpty\" \n\rGreetResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"5\n\x0fRegisterRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1e\n\x0bUserRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\",\n\x0cUserResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08username\x18\x02 \x01(\t\"\x1e\n\rTokenResponse\x12\r\n\x05token\x18\x01 \x01(\t\"\"\n\x0fGenericResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"$\n\x0eProductRequest\x12\x12\n\nproduct_id\x18\x01 \x01(\x05\"\x80\x01\n\x0fProductResponse\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x04 \x01(\t\x12\r\n\x05price\x18\x05 \x01(\x01\x12\x0e\n\x06slogan\x18\x06 \x01(\t\x12\r\n\x05stock\x18\x07 \x01(\x05\"C\n\x13ProductListResponse\x12,\n\x08products\x18\x01 \x03(\x0b\x32\x1a.dbservice.ProductResponse\"3\n\x0cOrderRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x12\n\nproduct_id\x18\x02 \x01(\x05\"1\n\rOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\x05\x12\x0e\n\x06status\x18\x02 \x01(\t2\x90\x05\n\tDBService\x12\x33\n\x05Greet\x12\x10.dbservice.Empty\x1a\x18.dbservice.GreetResponse\x12?\n\x08Register\x12\x1a.dbservice.RegisterRequest\x1a\x17.dbservice.UserResponse\x12>\n\tLoginUser\x12\x17.dbservice.LoginRequest\x1a\x18.dbservice.TokenResponse\x12:\n\x07GetUser\x12\x16.dbservice.UserRequest\x1a\x17.dbservice.UserResponse\x12\x44\n\x0e\x44\x65\x61\x63tivateUser\x12\x16.dbservice.UserRequest\x1a\x1a.dbservice.GenericResponse\x12@\n\x0cListProducts\x12\x10.dbservice.Empty\x1a\x1e.dbservice.ProductListResponse\x12\x43\n\nGetProduct\x12\x19.dbservice.ProductRequest\x1a\x1a.dbservice.ProductResponse\x12\x41\n\nPlaceOrder\x12\x17.dbservice.OrderRequest\x1a\x1a.dbservice.GenericResponse\x12\x42\n\x0b\x43\x61ncelOrder\x12\x17.dbservice.OrderRequest\x1a\x1a.dbservice.GenericResponse\x12=\n\x08GetOrder\x12\x17.dbservice.OrderRequest\x1a\x18.dbservice.OrderResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'db_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTY']._serialized_start=31
  _globals['_EMPTY']._serialized_end=38
  _globals['_GREETRESPONSE']._serialized_start=40
  _globals['_GREETRESPONSE']._serialized_end=72
  _globals['_REGISTERREQUEST']._serialized_start=74
  _globals['_REGISTERREQUEST']._serialized_end=127
  _globals['_LOGINREQUEST']._serialized_start=129
  _globals['_LOGINREQUEST']._serialized_end=179
  _globals['_USERREQUEST']._serialized_start=181
  _globals['_USERREQUEST']._serialized_end=211
  _globals['_USERRESPONSE']._serialized_start=213
  _globals['_USERRESPONSE']._serialized_end=257
  _globals['_TOKENRESPONSE']._serialized_start=259
  _globals['_TOKENRESPONSE']._serialized_end=289
  _globals['_GENERICRESPONSE']._serialized_start=291
  _globals['_GENERICRESPONSE']._serialized_end=325
  _globals['_PRODUCTREQUEST']._serialized_start=327
  _globals['_PRODUCTREQUEST']._serialized_end=363
  _globals['_PRODUCTRESPONSE']._serialized_start=366
  _globals['_PRODUCTRESPONSE']._serialized_end=494
  _globals['_PRODUCTLISTRESPONSE']._serialized_start=496
  _globals['_PRODUCTLISTRESPONSE']._serialized_end=563
  _globals['_ORDERREQUEST']._serialized_start=565
  _globals['_ORDERREQUEST']._serialized_end=616
  _globals['_ORDERRESPONSE']._serialized_start=618
  _globals['_ORDERRESPONSE']._serialized_end=667
  _globals['_DBSERVICE']._serialized_start=670
  _globals['_DBSERVICE']._serialized_end=1326
# @@protoc_insertion_point(module_scope)