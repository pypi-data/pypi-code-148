# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fsai_grpc_api/protos/detection_instance_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from fsai_grpc_api.protos import utils_pb2 as fsai__grpc__api_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='fsai_grpc_api/protos/detection_instance_api.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n1fsai_grpc_api/protos/detection_instance_api.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a fsai_grpc_api/protos/utils.proto\"\xb9\x03\n\x11\x44\x65tectionInstance\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x13\n\x0bworkflow_id\x18\x02 \x01(\x05\x12\x0f\n\x07part_id\x18\x03 \x01(\x05\x12\x10\n\x08image_id\x18\x04 \x01(\x05\x12\x1a\n\x08geo_bbox\x18\x05 \x01(\x0b\x32\x08.GeoBbox\x12\x14\n\x0c\x64\x65tection_id\x18\x06 \x01(\x05\x12\x11\n\tsource_id\x18\x07 \x01(\x05\x12\x1b\n\x13source_detection_id\x18\x08 \x01(\t\x12\r\n\x05score\x18\t \x01(\x02\x12\x0e\n\x06height\x18\n \x01(\x02\x12\x17\n\x0fheight_inferred\x18\x0b \x01(\x08\x12\x35\n\x11human_verified_at\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0b\x64\x65tected_at\x18\r \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\ncreated_at\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"V\n$FindOrCreateDetectionInstanceRequest\x12.\n\x12\x64\x65tection_instance\x18\x01 \x01(\x0b\x32\x12.DetectionInstance\"y\n%FindOrCreateDetectionInstanceResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12.\n\x12\x64\x65tection_instance\x18\x02 \x01(\x0b\x32\x12.DetectionInstance\"W\n%GetDetectionInstancesByImageIdRequest\x12.\n\x12\x64\x65tection_instance\x18\x01 \x01(\x0b\x32\x12.DetectionInstance\"{\n&GetDetectionInstancesByImageIdResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12/\n\x13\x64\x65tection_instances\x18\x02 \x03(\x0b\x32\x12.DetectionInstance\"W\n%UpdateDetectionInstanceGeoBboxRequest\x12.\n\x12\x64\x65tection_instance\x18\x01 \x01(\x0b\x32\x12.DetectionInstance\"z\n&UpdateDetectionInstanceGeoBboxResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12.\n\x12\x64\x65tection_instance\x18\x02 \x01(\x0b\x32\x12.DetectionInstance\"T\n\"DeleteDetectionInstanceByIdRequest\x12.\n\x12\x64\x65tection_instance\x18\x01 \x01(\x0b\x32\x12.DetectionInstance\"w\n#DeleteDetectionInstanceByIdResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12.\n\x12\x64\x65tection_instance\x18\x02 \x01(\x0b\x32\x12.DetectionInstance\"M\n\x1bSetHumanVerifiedByIdRequest\x12.\n\x12\x64\x65tection_instance\x18\x01 \x01(\x0b\x32\x12.DetectionInstance\"p\n\x1cSetHumanVerifiedByIdResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12.\n\x12\x64\x65tection_instance\x18\x02 \x01(\x0b\x32\x12.DetectionInstance2\xba\x04\n\x14\x44\x65tectionInstanceApi\x12n\n\x1d\x46indOrCreateDetectionInstance\x12%.FindOrCreateDetectionInstanceRequest\x1a&.FindOrCreateDetectionInstanceResponse\x12q\n\x1eGetDetectionInstancesByImageId\x12&.GetDetectionInstancesByImageIdRequest\x1a\'.GetDetectionInstancesByImageIdResponse\x12q\n\x1eUpdateDetectionInstanceGeoBbox\x12&.UpdateDetectionInstanceGeoBboxRequest\x1a\'.UpdateDetectionInstanceGeoBboxResponse\x12h\n\x1b\x44\x65leteDetectionInstanceById\x12#.DeleteDetectionInstanceByIdRequest\x1a$.DeleteDetectionInstanceByIdResponse\x12\x62\n#SetDetectionInstanceAsHumanVerified\x12\x1c.SetHumanVerifiedByIdRequest\x1a\x1d.SetHumanVerifiedByIdResponseb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,fsai__grpc__api_dot_protos_dot_utils__pb2.DESCRIPTOR,])




_DETECTIONINSTANCE = _descriptor.Descriptor(
  name='DetectionInstance',
  full_name='DetectionInstance',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='DetectionInstance.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='workflow_id', full_name='DetectionInstance.workflow_id', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='part_id', full_name='DetectionInstance.part_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='image_id', full_name='DetectionInstance.image_id', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='geo_bbox', full_name='DetectionInstance.geo_bbox', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detection_id', full_name='DetectionInstance.detection_id', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source_id', full_name='DetectionInstance.source_id', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='source_detection_id', full_name='DetectionInstance.source_detection_id', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='DetectionInstance.score', index=8,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height', full_name='DetectionInstance.height', index=9,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='height_inferred', full_name='DetectionInstance.height_inferred', index=10,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='human_verified_at', full_name='DetectionInstance.human_verified_at', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detected_at', full_name='DetectionInstance.detected_at', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='DetectionInstance.created_at', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='updated_at', full_name='DetectionInstance.updated_at', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=121,
  serialized_end=562,
)


_FINDORCREATEDETECTIONINSTANCEREQUEST = _descriptor.Descriptor(
  name='FindOrCreateDetectionInstanceRequest',
  full_name='FindOrCreateDetectionInstanceRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='FindOrCreateDetectionInstanceRequest.detection_instance', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=564,
  serialized_end=650,
)


_FINDORCREATEDETECTIONINSTANCERESPONSE = _descriptor.Descriptor(
  name='FindOrCreateDetectionInstanceResponse',
  full_name='FindOrCreateDetectionInstanceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='FindOrCreateDetectionInstanceResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='FindOrCreateDetectionInstanceResponse.detection_instance', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=652,
  serialized_end=773,
)


_GETDETECTIONINSTANCESBYIMAGEIDREQUEST = _descriptor.Descriptor(
  name='GetDetectionInstancesByImageIdRequest',
  full_name='GetDetectionInstancesByImageIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='GetDetectionInstancesByImageIdRequest.detection_instance', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=775,
  serialized_end=862,
)


_GETDETECTIONINSTANCESBYIMAGEIDRESPONSE = _descriptor.Descriptor(
  name='GetDetectionInstancesByImageIdResponse',
  full_name='GetDetectionInstancesByImageIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='GetDetectionInstancesByImageIdResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detection_instances', full_name='GetDetectionInstancesByImageIdResponse.detection_instances', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=864,
  serialized_end=987,
)


_UPDATEDETECTIONINSTANCEGEOBBOXREQUEST = _descriptor.Descriptor(
  name='UpdateDetectionInstanceGeoBboxRequest',
  full_name='UpdateDetectionInstanceGeoBboxRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='UpdateDetectionInstanceGeoBboxRequest.detection_instance', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=989,
  serialized_end=1076,
)


_UPDATEDETECTIONINSTANCEGEOBBOXRESPONSE = _descriptor.Descriptor(
  name='UpdateDetectionInstanceGeoBboxResponse',
  full_name='UpdateDetectionInstanceGeoBboxResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='UpdateDetectionInstanceGeoBboxResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='UpdateDetectionInstanceGeoBboxResponse.detection_instance', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1078,
  serialized_end=1200,
)


_DELETEDETECTIONINSTANCEBYIDREQUEST = _descriptor.Descriptor(
  name='DeleteDetectionInstanceByIdRequest',
  full_name='DeleteDetectionInstanceByIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='DeleteDetectionInstanceByIdRequest.detection_instance', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1202,
  serialized_end=1286,
)


_DELETEDETECTIONINSTANCEBYIDRESPONSE = _descriptor.Descriptor(
  name='DeleteDetectionInstanceByIdResponse',
  full_name='DeleteDetectionInstanceByIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='DeleteDetectionInstanceByIdResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='DeleteDetectionInstanceByIdResponse.detection_instance', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1288,
  serialized_end=1407,
)


_SETHUMANVERIFIEDBYIDREQUEST = _descriptor.Descriptor(
  name='SetHumanVerifiedByIdRequest',
  full_name='SetHumanVerifiedByIdRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='SetHumanVerifiedByIdRequest.detection_instance', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1409,
  serialized_end=1486,
)


_SETHUMANVERIFIEDBYIDRESPONSE = _descriptor.Descriptor(
  name='SetHumanVerifiedByIdResponse',
  full_name='SetHumanVerifiedByIdResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='SetHumanVerifiedByIdResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='detection_instance', full_name='SetHumanVerifiedByIdResponse.detection_instance', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1488,
  serialized_end=1600,
)

_DETECTIONINSTANCE.fields_by_name['geo_bbox'].message_type = fsai__grpc__api_dot_protos_dot_utils__pb2._GEOBBOX
_DETECTIONINSTANCE.fields_by_name['human_verified_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_DETECTIONINSTANCE.fields_by_name['detected_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_DETECTIONINSTANCE.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_DETECTIONINSTANCE.fields_by_name['updated_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_FINDORCREATEDETECTIONINSTANCEREQUEST.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_FINDORCREATEDETECTIONINSTANCERESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
_FINDORCREATEDETECTIONINSTANCERESPONSE.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_GETDETECTIONINSTANCESBYIMAGEIDREQUEST.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_GETDETECTIONINSTANCESBYIMAGEIDRESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
_GETDETECTIONINSTANCESBYIMAGEIDRESPONSE.fields_by_name['detection_instances'].message_type = _DETECTIONINSTANCE
_UPDATEDETECTIONINSTANCEGEOBBOXREQUEST.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_UPDATEDETECTIONINSTANCEGEOBBOXRESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
_UPDATEDETECTIONINSTANCEGEOBBOXRESPONSE.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_DELETEDETECTIONINSTANCEBYIDREQUEST.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_DELETEDETECTIONINSTANCEBYIDRESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
_DELETEDETECTIONINSTANCEBYIDRESPONSE.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_SETHUMANVERIFIEDBYIDREQUEST.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
_SETHUMANVERIFIEDBYIDRESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
_SETHUMANVERIFIEDBYIDRESPONSE.fields_by_name['detection_instance'].message_type = _DETECTIONINSTANCE
DESCRIPTOR.message_types_by_name['DetectionInstance'] = _DETECTIONINSTANCE
DESCRIPTOR.message_types_by_name['FindOrCreateDetectionInstanceRequest'] = _FINDORCREATEDETECTIONINSTANCEREQUEST
DESCRIPTOR.message_types_by_name['FindOrCreateDetectionInstanceResponse'] = _FINDORCREATEDETECTIONINSTANCERESPONSE
DESCRIPTOR.message_types_by_name['GetDetectionInstancesByImageIdRequest'] = _GETDETECTIONINSTANCESBYIMAGEIDREQUEST
DESCRIPTOR.message_types_by_name['GetDetectionInstancesByImageIdResponse'] = _GETDETECTIONINSTANCESBYIMAGEIDRESPONSE
DESCRIPTOR.message_types_by_name['UpdateDetectionInstanceGeoBboxRequest'] = _UPDATEDETECTIONINSTANCEGEOBBOXREQUEST
DESCRIPTOR.message_types_by_name['UpdateDetectionInstanceGeoBboxResponse'] = _UPDATEDETECTIONINSTANCEGEOBBOXRESPONSE
DESCRIPTOR.message_types_by_name['DeleteDetectionInstanceByIdRequest'] = _DELETEDETECTIONINSTANCEBYIDREQUEST
DESCRIPTOR.message_types_by_name['DeleteDetectionInstanceByIdResponse'] = _DELETEDETECTIONINSTANCEBYIDRESPONSE
DESCRIPTOR.message_types_by_name['SetHumanVerifiedByIdRequest'] = _SETHUMANVERIFIEDBYIDREQUEST
DESCRIPTOR.message_types_by_name['SetHumanVerifiedByIdResponse'] = _SETHUMANVERIFIEDBYIDRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

DetectionInstance = _reflection.GeneratedProtocolMessageType('DetectionInstance', (_message.Message,), {
  'DESCRIPTOR' : _DETECTIONINSTANCE,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:DetectionInstance)
  })
_sym_db.RegisterMessage(DetectionInstance)

FindOrCreateDetectionInstanceRequest = _reflection.GeneratedProtocolMessageType('FindOrCreateDetectionInstanceRequest', (_message.Message,), {
  'DESCRIPTOR' : _FINDORCREATEDETECTIONINSTANCEREQUEST,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:FindOrCreateDetectionInstanceRequest)
  })
_sym_db.RegisterMessage(FindOrCreateDetectionInstanceRequest)

FindOrCreateDetectionInstanceResponse = _reflection.GeneratedProtocolMessageType('FindOrCreateDetectionInstanceResponse', (_message.Message,), {
  'DESCRIPTOR' : _FINDORCREATEDETECTIONINSTANCERESPONSE,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:FindOrCreateDetectionInstanceResponse)
  })
_sym_db.RegisterMessage(FindOrCreateDetectionInstanceResponse)

GetDetectionInstancesByImageIdRequest = _reflection.GeneratedProtocolMessageType('GetDetectionInstancesByImageIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETDETECTIONINSTANCESBYIMAGEIDREQUEST,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:GetDetectionInstancesByImageIdRequest)
  })
_sym_db.RegisterMessage(GetDetectionInstancesByImageIdRequest)

GetDetectionInstancesByImageIdResponse = _reflection.GeneratedProtocolMessageType('GetDetectionInstancesByImageIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETDETECTIONINSTANCESBYIMAGEIDRESPONSE,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:GetDetectionInstancesByImageIdResponse)
  })
_sym_db.RegisterMessage(GetDetectionInstancesByImageIdResponse)

UpdateDetectionInstanceGeoBboxRequest = _reflection.GeneratedProtocolMessageType('UpdateDetectionInstanceGeoBboxRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDETECTIONINSTANCEGEOBBOXREQUEST,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:UpdateDetectionInstanceGeoBboxRequest)
  })
_sym_db.RegisterMessage(UpdateDetectionInstanceGeoBboxRequest)

UpdateDetectionInstanceGeoBboxResponse = _reflection.GeneratedProtocolMessageType('UpdateDetectionInstanceGeoBboxResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEDETECTIONINSTANCEGEOBBOXRESPONSE,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:UpdateDetectionInstanceGeoBboxResponse)
  })
_sym_db.RegisterMessage(UpdateDetectionInstanceGeoBboxResponse)

DeleteDetectionInstanceByIdRequest = _reflection.GeneratedProtocolMessageType('DeleteDetectionInstanceByIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEDETECTIONINSTANCEBYIDREQUEST,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:DeleteDetectionInstanceByIdRequest)
  })
_sym_db.RegisterMessage(DeleteDetectionInstanceByIdRequest)

DeleteDetectionInstanceByIdResponse = _reflection.GeneratedProtocolMessageType('DeleteDetectionInstanceByIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _DELETEDETECTIONINSTANCEBYIDRESPONSE,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:DeleteDetectionInstanceByIdResponse)
  })
_sym_db.RegisterMessage(DeleteDetectionInstanceByIdResponse)

SetHumanVerifiedByIdRequest = _reflection.GeneratedProtocolMessageType('SetHumanVerifiedByIdRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETHUMANVERIFIEDBYIDREQUEST,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:SetHumanVerifiedByIdRequest)
  })
_sym_db.RegisterMessage(SetHumanVerifiedByIdRequest)

SetHumanVerifiedByIdResponse = _reflection.GeneratedProtocolMessageType('SetHumanVerifiedByIdResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETHUMANVERIFIEDBYIDRESPONSE,
  '__module__' : 'fsai_grpc_api.protos.detection_instance_api_pb2'
  # @@protoc_insertion_point(class_scope:SetHumanVerifiedByIdResponse)
  })
_sym_db.RegisterMessage(SetHumanVerifiedByIdResponse)



_DETECTIONINSTANCEAPI = _descriptor.ServiceDescriptor(
  name='DetectionInstanceApi',
  full_name='DetectionInstanceApi',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1603,
  serialized_end=2173,
  methods=[
  _descriptor.MethodDescriptor(
    name='FindOrCreateDetectionInstance',
    full_name='DetectionInstanceApi.FindOrCreateDetectionInstance',
    index=0,
    containing_service=None,
    input_type=_FINDORCREATEDETECTIONINSTANCEREQUEST,
    output_type=_FINDORCREATEDETECTIONINSTANCERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetDetectionInstancesByImageId',
    full_name='DetectionInstanceApi.GetDetectionInstancesByImageId',
    index=1,
    containing_service=None,
    input_type=_GETDETECTIONINSTANCESBYIMAGEIDREQUEST,
    output_type=_GETDETECTIONINSTANCESBYIMAGEIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='UpdateDetectionInstanceGeoBbox',
    full_name='DetectionInstanceApi.UpdateDetectionInstanceGeoBbox',
    index=2,
    containing_service=None,
    input_type=_UPDATEDETECTIONINSTANCEGEOBBOXREQUEST,
    output_type=_UPDATEDETECTIONINSTANCEGEOBBOXRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteDetectionInstanceById',
    full_name='DetectionInstanceApi.DeleteDetectionInstanceById',
    index=3,
    containing_service=None,
    input_type=_DELETEDETECTIONINSTANCEBYIDREQUEST,
    output_type=_DELETEDETECTIONINSTANCEBYIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetDetectionInstanceAsHumanVerified',
    full_name='DetectionInstanceApi.SetDetectionInstanceAsHumanVerified',
    index=4,
    containing_service=None,
    input_type=_SETHUMANVERIFIEDBYIDREQUEST,
    output_type=_SETHUMANVERIFIEDBYIDRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DETECTIONINSTANCEAPI)

DESCRIPTOR.services_by_name['DetectionInstanceApi'] = _DETECTIONINSTANCEAPI

# @@protoc_insertion_point(module_scope)
