# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: assistant.proto
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
    'assistant.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x61ssistant.proto\"6\n\x0cGreetRequest\x12\x11\n\tuser_name\x18\x01 \x01(\t\x12\x13\n\x0binstitution\x18\x02 \x01(\t\" \n\rGreetResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"\'\n\x0bMultRequest\x12\x0b\n\x03xin\x18\x01 \x01(\x01\x12\x0b\n\x03yin\x18\x02 \x01(\x01\"8\n\x0cMultResponse\x12\x0b\n\x03xin\x18\x01 \x01(\x01\x12\x0b\n\x03yin\x18\x02 \x01(\x01\x12\x0e\n\x06result\x18\x03 \x01(\x01\x32k\n\x10\x41ssistantService\x12.\n\rGreetWithInfo\x12\r.GreetRequest\x1a\x0e.GreetResponse\x12\'\n\x08Multiply\x12\x0c.MultRequest\x1a\r.MultResponseB\x06Z\x04./pbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'assistant_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\004./pb'
  _globals['_GREETREQUEST']._serialized_start=19
  _globals['_GREETREQUEST']._serialized_end=73
  _globals['_GREETRESPONSE']._serialized_start=75
  _globals['_GREETRESPONSE']._serialized_end=107
  _globals['_MULTREQUEST']._serialized_start=109
  _globals['_MULTREQUEST']._serialized_end=148
  _globals['_MULTRESPONSE']._serialized_start=150
  _globals['_MULTRESPONSE']._serialized_end=206
  _globals['_ASSISTANTSERVICE']._serialized_start=208
  _globals['_ASSISTANTSERVICE']._serialized_end=315
# @@protoc_insertion_point(module_scope)