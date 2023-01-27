# -*- coding: utf-8 -*- --------------------------------------------------===#
#
#  Copyright 2018-2023 Trovares Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===----------------------------------------------------------------------===#

import logging

import grpc
import ipaddress
import pandas as pd
import pyarrow
import sys

from . import DataService_pb2 as data_proto
from . import ErrorMessages_pb2 as err_proto

log = logging.getLogger(__name__)

BOOLEAN = 'boolean'
INT = 'int'
FLOAT = 'float'
DATE = 'date'
TIME = 'time'
DATETIME = 'datetime'
IPADDRESS = 'ipaddress'
TEXT = 'text'
LIST = 'list'
ROWID = 'row_id'
DURATION = 'duration'

# Send in 2MB chunks (grpc recommends 16-64 KB, but this got the best
# performance locally).  By default grpc only supports up to 4MB.
MAX_PACKET_SIZE = 2097152

class XgtError(Exception):
  """
  Base exception class from which all other xgt exceptions inherit. It is
  raised in error cases that don't have a specific xgt exception type.
  """
  def __init__(self, msg, trace=''):
    self.msg = msg
    self.trace = trace

    if log.getEffectiveLevel() >= logging.DEBUG:
      if self.trace != '':
        log.debug(self.trace)
      else:
        log.debug(self.msg)
    Exception.__init__(self, self.msg)

class XgtNotImplemented(XgtError):
  """Raised for functionality with pending implementation."""
class XgtInternalError(XgtError):
  """
  Intended for internal server purposes only. This exception should not become
  visible to the user.
  """
class XgtIOError(XgtError):
  """An I/O problem occurred either on the client or server side."""
  def __init__(self, msg, trace='', job = None):
    self._job = job
    XgtError.__init__(self, msg, trace)

  @property
  def job(self):
    """
    Job: Job associated with the load/insert operation if available. May be
    None.
    """
    return self._job
class XgtServerMemoryError(XgtError):
  """
  The server memory usage is close to or at capacity and work could be lost.
  """
class XgtConnectionError(XgtError):
  """
  The client cannot properly connect to the server. This can include a failure
  to connect due to an xgt module version error.
  """
class XgtSyntaxError(XgtError):
  """A query was provided with incorrect syntax."""
class XgtTypeError(XgtError):
  """
  An unexpected type was supplied.

  For queries, an invalid data type was used either as an entity or as a
  property. For frames, either an edge, vertex or table frames was expected
  but the wrong frame type or some other data type was provided. For
  properties, the property declaration establishes the expected data type. A
  type error is raise if the data type used is not appropriate.
  """
class XgtValueError(XgtError):
  """An invalid or unexpected value was provided."""
class XgtNameError(XgtError):
  """
  An unexpected name was provided. Typically can occur during object retrieval
  where the object name was not found.
  """
class XgtArithmeticError(XgtError):
  """An invalid arithmetic calculation was detected and cannot be handled."""
class XgtFrameDependencyError(XgtError):
  """
  The requested action will produce an invalid graph or break a valid graph.
  """
class XgtTransactionError(XgtError):
  """A Transaction was attempted but didn't complete."""
class XgtSecurityError(XgtError):
  """A security violation occured."""

class _ContainerMap:
  """
  Maps container ids to frames.
  The user shouldn't manually construct this.

  Parameters
  ----------
  conn : Connection
    xgt Connection.
  container_dict : dictionary
    Dictionary containing keys of container ids to map.
    If empty is given, will map all frames.

  """
  def __init__(self, conn, container_dict = {}):
    self.frames = { }
    table_frames = conn.get_table_frames()
    vertex_frames = conn.get_vertex_frames()
    edge_frames = conn.get_edge_frames()

    for frame in table_frames:
      if not container_dict or frame._container_id in container_dict:
        self.frames[frame._container_id] = frame

    for frame in vertex_frames:
      if not container_dict or frame._container_id in container_dict:
        self.frames[frame._container_id] = frame

    for frame in edge_frames:
      if not container_dict or frame._container_id in container_dict:
        self.frames[frame._container_id] = frame

  # The row id is in serialized form. The form is explained below in class Row.
  def get_data(self, row_id, include_row_labels = False):
    vals = row_id.split(' ')
    container_id = int(vals[2])
    row_pos = int(vals[3])
    row_delete_id = int(vals[4])
    if container_id in self.frames:
      return self.frames[container_id]._get_data(
          row_pos, length = 1, include_row_labels = include_row_labels,
          validation_id = row_delete_id)[0]
    return None

class Row:
  """
  Row represents a row returned from a server such as a path.
  The user shouldn't manually construct these.

  Parameters
  ----------
  container_map : _ContainerMap
    Map of container ids to frames.
  row_id : string
    String in serialized form: 'RowID: X Y Z' where X is the container id,
    Y is the row position, and Z is commit id when this value was valid.

  """
  def __init__(self, container_map, row_id):
    self.container_map = container_map
    self.row_id = row_id

  def get_data(self, include_row_labels = False):
    """
    Returns row data. If the frame this row points to has deletions this row
    is considered invalid and will raise an exception.

    Parameters
    ----------
    include_row_labels : bool
      Indicates whether the security labels for each row should be egested
      along with the row.

    Returns
    -------
    list

    Raises
    -------
    XgtNameError
      If the frame does not exist on the server.
    XgtSecurityError
      If the user does not have required permissions for this action.
    XgtTransactionError
      If a conflict with another transaction occurs.
    ValueError
      If parameter is out of bounds or the row is no longer valid due to a
      transactional update.

    """
    return self.container_map.get_data(self.row_id, include_row_labels)

  def __str__(self):
    return "{ROW: " + str(self.get_data()) + "}"

  def __repr__(self):
    return str(self)

  def __lt__(self, obj):
    return ((self.get_data()) < (obj.get_data()))

  def serialize(self):
    return row_id

# Validation support functions

def _validated_schema(obj):
  '''Takes a user-supplied object and returns a valid schema.

  Users can supply a variety of objects as valid schemas. To simplify internal
  processing, we canonicalize these into a list of string-type pairs,
  performing validation along the way.
  '''
  # Validate the shape first
  try:
    if len(obj) < 1:
      raise XgtTypeError('A schema must not be empty.')
    for col in obj:
      assert len(col) >= 2
      if _validated_property_type(col[1]) == "LIST":
        assert (len(col) <= 4 and len(col) >= 3)
      else:
        assert len(col) == 2
  except:
    raise XgtTypeError('A schema must be a non-empty list of (property, ' +
                       'type) pairs.')
  # Looks good. Return a canonical schema.
  schema_returned = []
  for col in obj:
    val_type = _validated_property_type(col[1])
    if val_type != "LIST":
      schema_returned.append((_validated_property_name(col[0]), val_type))
    else:
      leaf_type = _validated_property_type(col[2])
      if len(col) != 4:
        schema_returned.append((_validated_property_name(col[0]),
                               val_type, leaf_type))
      else:
        schema_returned.append((_validated_property_name(col[0]),
                                val_type, leaf_type, col[3]))
  return schema_returned

def _validated_frame_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  _assert_isstring(obj)
  name = str(obj)
  if len(name) < 1:
    raise XgtNameError('Frame names cannot be empty.')
  return name

def _validated_namespace_name(obj):
  '''Takes a user-supplied object and returns a unicode frame name string.'''
  _assert_isstring(obj)
  name = str(obj)
  if len(name) < 1:
    raise XgtNameError('Namespace names cannot be empty.')
  return name

def _validated_property_name(obj):
  '''Takes a user-supplied object and returns a unicode property name string.'''
  _assert_isstring(obj)
  return str(obj)

def _get_valid_property_types_to_create():
  return [BOOLEAN, INT, FLOAT, DATE, TIME, DATETIME, IPADDRESS, TEXT,
          LIST, ROWID, DURATION]

def _get_valid_property_types_for_return_only():
  return ['container_id', 'job_id']

def _validated_property_type(obj):
  '''Takes a user-supplied object and returns an xGT schema type.'''
  _assert_isstring(obj)
  prop_type = str(obj)
  valid_prop_types = _get_valid_property_types_to_create()
  if prop_type.lower() not in valid_prop_types:
    if prop_type.lower in _get_valid_property_types_for_return_only():
      raise XgtTypeError('Invalid property type "'+prop_type+'". This type '
                         'cannot be used when creating a frame.')
    else:
      raise XgtTypeError('Invalid property type "'+prop_type+'"')
  return prop_type.upper()

def _validate_opt_level(optlevel):
  """
  Valid optimization level values are:
    - 0: No optimization.
    - 1: General optimization.
    - 2: WHERE-clause optimization.
    - 3: Degree-cycle optimization.
    - 4: Query order optimization.
  """
  if isinstance(optlevel, int):
    if optlevel not in [0, 1, 2, 3, 4]:
      raise XgtValueError("Invalid optlevel '" + str(optlevel) +"'")
  else:
    raise XgtTypeError("optlevel must be an integer")
  return True

def _assert_noerrors(response):
  if len(response.error) > 0:
    error = response.error[0]
    try:
      error_code_name = err_proto.ErrorCodeEnum.Name(error.code)
      error_class = _code_error_map[error_code_name]
      raise error_class(error.message, error.detail)
    except XgtError:
      raise
    except Exception as ex:
      raise XgtError("Error detected while raising exception" +
                     str(ex), str(ex))

def _convert_flight_server_error_into_xgt(error):
  if len(error.extra_info) >= 8 and error.extra_info[0:6] == b"ERROR:":
    try:
      error_class = _code_error_map[
          err_proto.ErrorCodeEnum.Name(int(error.extra_info[6:8]))]
      return error_class(str(error), error.extra_info)
    except:
      pass
  return XgtError(str(error))

def _assert_isstring(value):
  if not isinstance(value, str):
    msg = str(value) + " is not a string"
    raise TypeError(msg)

_code_error_map = {
  'GENERIC_ERROR': XgtError,
  'NOT_IMPLEMENTED': XgtNotImplemented,
  'INTERNAL_ERROR': XgtInternalError,
  'IO_ERROR': XgtIOError,
  'SERVER_MEMORY_ERROR': XgtServerMemoryError,
  'CONNECTION_ERROR': XgtConnectionError,
  'SYNTAX_ERROR': XgtSyntaxError,
  'TYPE_ERROR': XgtTypeError,
  'VALUE_ERROR': XgtValueError,
  'NAME_ERROR': XgtNameError,
  'ARITHMETIC_ERROR': XgtArithmeticError,
  'FRAME_DEPENDENCY_ERROR': XgtFrameDependencyError,
  'TRANSACTION_ERROR': XgtTransactionError,
  'SECURITY_ERROR': XgtSecurityError,
}

def _verify_offset_length(offset, length):
  max_uint64 = sys.maxsize * 2 + 1

  if isinstance(offset, str):
    offset = int(offset)
  if not isinstance(offset, int) or offset < 0:
    raise XgtValueError("offset must be a non-negative integer.")
  if offset > max_uint64:
    raise XgtValueError(f"offset must be < {max_uint64}")

  if length is not None:
    if isinstance(length, str):
      length = int(length)
    if not isinstance(length, int) or length < 0:
      raise XgtValueError("length must be a non-negative integer.")
    if length > max_uint64:
      raise XgtValueError(f"length must be < {max_uint64}")

  return offset, length

def _create_flight_ticket(name, offset, length, include_row_labels,
                          row_label_column_header = None,
                          order = True, date_as_string = False,
                          job_id = None, validation_id = None,
                          duration_as_interval = False):
  offset, length = _verify_offset_length(offset, length)

  ticket = '`' + name + '`'

  if offset != 0:
    ticket += ".offset=" + str(offset)
  if length != None:
    ticket += ".length=" + str(length)
  if order:
    ticket += ".order=True"
  if date_as_string:
    ticket += ".dates_as_strings=True"
  if include_row_labels:
    ticket += ".egest_row_labels=True"
  if row_label_column_header is not None:
    ticket += ".label_column_header=" + row_label_column_header
  if validation_id is not None:
    ticket += ".validation_id=" + str(validation_id)
  if duration_as_interval:
    ticket += ".duration_as_interval=True"

  if job_id is not None:
    if isinstance(job_id, str):
      job_id = int(job_id)
    elif not isinstance(job_id, int):
      raise ValueError("job ID must be an int.")
    ticket += ".job_id=" + str(job_id)

  return ticket

def _convert_row_id_list(container_map, value, depth = 0):
  if value is None:
    return None
  elif depth > 1:
    return [_convert_row_id_list(container_map, list_val, depth - 1)
            if list_val != None else None for list_val in value]
  else:
    return [Row(container_map, id_val) if id_val != None else None
            for id_val in value]

def _convert_ip_address_list(value, depth = 1):
  if value is None:
    return None
  elif depth > 1:
    return [_convert_ip_address_list(list_val, depth - 1)
            if list_val is not None else None for list_val in value]
  else:
    return [ipaddress.ip_address(id_val) if id_val is not None else None
            for id_val in value]

# Creates a list of conversion functions from the schema.
# Currently has conversions for row id and paths(row id lists).
def _schema_row_conversion(schema, conn):
  conversion_funcs = []
  container_map = None

  for entry in schema:
    if entry[1] == IPADDRESS:
      def closure(value):
        return ipaddress.ip_address(value) if value is not None else None
      conversion_funcs.append(closure)
    elif(entry[1] == LIST and entry[2] == IPADDRESS):
      if len(entry) == 3:
        def closure(value):
          return _convert_ip_address_list(value)
        conversion_funcs.append(closure)
      else:
        def closure(value):
          return _convert_ip_address_list(value, entry[3])
        conversion_funcs.append(closure)
    elif entry[1] == ROWID:
      if container_map == None:
        container_map = _ContainerMap(conn)
      def closure(value):
        # TODO(Greg): Doesn't this return a list instead of a single value?
        return _convert_row_id_list(container_map, value)
      conversion_funcs.append(closure)
    elif(entry[1] == LIST and entry[2] == ROWID):
      if len(entry) == 3:
        if container_map == None:
          container_map = _ContainerMap(conn)
        def closure(value):
          return _convert_row_id_list(container_map, value, 1)
        conversion_funcs.append(closure)
      else:
        if container_map == None:
          container_map = _ContainerMap(conn)
        def closure(value):
          return _convert_row_id_list(container_map, value, entry[3])
        conversion_funcs.append(closure)
    else:
      conversion_funcs.append(None)

  return conversion_funcs

def _get_data_python_from_table(arrow_table, schema, conn):
  if arrow_table is None:
    return None

  # Get functions used to convert columns coming from the server.
  # Currently, this provides functions for converting paths(lists of row ids)
  # and row ids into the Row class.
  conversion_funcs = _schema_row_conversion(schema, conn)

  # List comprehension here is simpler, but has slow performance due to the
  # access pattern being bad for the cache hits.
  return_list = [None] * arrow_table.num_rows
  if arrow_table.num_columns > len(conversion_funcs):
    conversion_funcs += [None] * (arrow_table.num_columns -
                                  len(conversion_funcs))

  for i in range(arrow_table.num_rows):
    return_list[i] = []
  for i, x in enumerate(arrow_table):
    if conversion_funcs[i] == None:
      for j, y in enumerate(x):
        return_list[j].append(y.as_py())
    else:
      for j, y in enumerate(x):
        return_list[j].append(conversion_funcs[i](y.as_py()))

  return return_list

def _get_data_pandas_from_table(arrow_table, schema, conn):
  if arrow_table is None:
    return None

  pandas_dict = {}
  for i, (name, col) in enumerate(zip(arrow_table.column_names, arrow_table)):
    if i < len(schema) and schema[i][1] == IPADDRESS:
      pandas_dict[name] = \
          pd.Series([None if x.as_py() is None else ipaddress.ip_address(x)
                     for x in col], dtype = 'object')
    elif i < len(schema) and schema[i][1] == LIST and schema[i][2] == IPADDRESS:
      depth = 1 if len(schema[i]) == 3 else schema[i][3]

      pandas_dict[name] = \
          pd.Series([_convert_ip_address_list(x.as_py(), depth) for x in col],
                    dtype = 'object')
    else:
      pandas_dict[name] = col.to_pandas()

  return pd.DataFrame(pandas_dict)

def _get_data_arrow(conn, ticket):
  try:
    res_table = conn.arrow_conn.do_get(pyarrow.flight.Ticket(ticket)).read_all()
    return res_table
  except pyarrow._flight.FlightServerError as err:
    raise _convert_flight_server_error_into_xgt(err) from err
  except pyarrow._flight.FlightUnavailableError as err:
    raise XgtConnectionError(str(err)) from err

def _get_data_python(conn, ticket, schema):
  res_table = _get_data_arrow(conn, ticket)
  return _get_data_python_from_table(res_table, schema, conn)

def _get_data_pandas(conn, ticket, schema):
  res_table = _get_data_arrow(conn, ticket)
  return _get_data_pandas_from_table(res_table, schema, conn)

# Helper functions for low code.

# Convert the pyarrow type to an xgt type.
def _pyarrow_type_to_xgt_type(pyarrow_type, depth = 0):
  if pyarrow.types.is_boolean(pyarrow_type):
    return (BOOLEAN, depth)
  elif (pyarrow.types.is_timestamp(pyarrow_type) or
        pyarrow.types.is_date64(pyarrow_type)):
    return (DATETIME, depth)
  elif pyarrow.types.is_date(pyarrow_type):
    return (DATE, depth)
  elif pyarrow.types.is_time(pyarrow_type):
    return (TIME, depth)
  elif pyarrow.types.is_temporal(pyarrow_type):
    return (DURATION, depth)
  elif pyarrow.types.is_integer(pyarrow_type):
    return (INT, depth)
  elif (pyarrow.types.is_float32(pyarrow_type) or
        pyarrow.types.is_float64(pyarrow_type) or
        pyarrow.types.is_decimal(pyarrow_type)):
    return (FLOAT, depth)
  elif pyarrow.types.is_string(pyarrow_type):
    return (TEXT, depth)
  elif (pyarrow.types.is_list(pyarrow_type) or
        pyarrow.types.is_large_list(pyarrow_type)):
    return _pyarrow_type_to_xgt_type(pyarrow_type.value_type, depth + 1)
  else:
    raise XgtTypeError("Cannot convert pyarrow type " + str(pyarrow_type) + " to xGT type.")

def _infer_xgt_schema_from_pyarrow_schema(pyarrow_schema):
  xgt_schema = []
  for c in pyarrow_schema:
    xgt_type = _pyarrow_type_to_xgt_type(c.type)
    if xgt_type[1] == 0:
      xgt_schema.append([c.name, xgt_type[0]])
    else:
      xgt_schema.append([c.name, LIST, xgt_type[0], xgt_type[1]])
  return xgt_schema

# Get the column in the schema by name or position.
def _find_key_in_schema(key, schema):
  if isinstance(key, str):
    found_key = False
    for elem in schema:
      if elem[0] == key:
        found_key = True
        break
    if not found_key:
      raise XgtNameError("The key " + str(key) + " not found in schema: " + str(schema))
    return key
  elif isinstance(key, int):
    if key >= len(schema) or key < 0:
      raise XgtError("Could not locate key " + str(key) + " in schema with " + str(len(schema)) + " entries.")
    return schema[key][0]

# Modify an xgt schema based on a frame column name to data column name
# mapping. The key names of this map will become the column names of the
# new schema. The values of the map correspond to the columns of the
# initial schema.
def _apply_mapping_to_schema(initial_schema, frame_to_data_column_mapping):
  def find_data_col_name(data_col):
    if isinstance(data_col, str):
      return data_col
    elif isinstance(data_col, int):
      if data_col >= len(initial_schema) or data_col < 0:
        err = "Error creating the schema. The column mapping refers to data column " + \
              "position " + str(data_col) + ", but only " + str(len(initial_schema)) + \
              " columns were found in the data."
        raise XgtValueError(err)
      return initial_schema[data_col][0]

  data_col_name_to_type = { elem[0] : elem[1] for elem in initial_schema }

  schema = []
  for frame_col, data_col in frame_to_data_column_mapping.items():
    data_type = data_col_name_to_type[find_data_col_name(data_col)]
    schema.append([frame_col, data_type])

  return schema

def _remove_label_columns_from_schema(initial_schema, row_label_columns):
  def find_data_col_name(data_col):
    if isinstance(data_col, str):
      return data_col
    elif isinstance(data_col, int):
      if data_col >= len(initial_schema) or data_col < 0:
        err = ("Error creating the schema. The row_label_columns parameter refers to data column " +
               "position " + str(data_col) + ", but only " + str(len(initial_schema)) +
               " columns were found in the data.")
        raise XgtValueError(err)
      return initial_schema[data_col][0]

  data_col_name_to_type = { elem[0] : elem[1] for elem in initial_schema }

  label_columns = set([find_data_col_name(col) for col in row_label_columns])

  return [col for col in initial_schema if col[0] not in label_columns]
