# import typing
# from typing import Any, Dict, List, Tuple, Type, Union

# from anton.type_match import do_the_types_match


# class TypeHandler:
#     def does_type_match(self, value: Any, parameter_type: Type) -> bool:
#         ...

#     def generate_object(self, value: Any, parameter_type: Type) -> Any:
#         ...

#     def get_value(self, value: Any, parameter_type: Type) -> Any:
#         if not self.does_type_match(value, parameter_type):
#             raise TypeError(f"{value} is not of type {parameter_type}.")
#         return self.generate_object(value, parameter_type)


# class PrimitiveTypeHandler(TypeHandler):
#     def does_type_match(self, value: Any, parameter_type: Type) -> bool:
#         return isinstance(value, parameter_type)

#     def generate_object(self, value: Any, parameter_type: Type) -> Any:
#         return value


# class AnyHandler(PrimitiveTypeHandler):
#     primitive_type: Type = Any


# class UnionHandler(TypeHandler):
#     def does_type_match(self, value: Any, parameter_type: Type) -> bool:
#         union_types = typing.get_args(parameter_type)
#         return isinstance(value, union_types)

#     def generate_object(self, value: Any, parameter_type: Type) -> Any:
#         return value


# class ListHandler(TypeHandler):
#     def does_type_match(self, value: Any, parameter_type: Type) -> bool:
#         list_elements_type = typing.get_args(parameter_type)[0]
#         container_obeys_type = isinstance(value, List)

#         list_element_type_handler: TypeHandler = TYPE_HANDLER_REGISTER[list_elements_type]
#         elements_obey_type = all(
#             [list_element_type_handler.does_type_match(element, list_elements_type) for element in value]
#         )
#         return container_obeys_type and elements_obey_type

#     def generate_object(self, value: Any, parameter_type: Type) -> Any:
#         return value


# class TupleHandler(TypeHandler):
#     def single_type_case(self, value: Any, parameter_type: Type) -> bool:
#         type_handler: TypeHandler = TYPE_HANDLER_REGISTER[parameter_type]
#         return all([type_handler.does_type_match(element, parameter_type) for element in value])

#     def multi_type_case(self, value: Any, tuple_elements_type: Tuple[Type, ...]) -> bool:
#         if len(tuple_elements_type) != len(value):
#             return False

#         return all(
#             [
#                 TYPE_HANDLER_REGISTER[element_type].does_type_match(element, element_type)
#                 for element, element_type in zip(value, tuple_elements_type)
#             ]
#         )

#     def does_type_match(self, value: Any, parameter_type: Type) -> bool:
#         # We recieve the value as `List` althought the type will be `Tuple`. Hence testing against type List.
#         # Tuple can have two ways of typing.
#         #   - Tuple[T_1, T_2, ....., T_n] : For `i` assert do_the_types_match(value[i], T_i)
#         #   - Tuple[T, ...]               : For `i` assert do_the_types_match(value[i], T)

#         container_obeys_type = isinstance(value, List)
#         tuple_elements_type = typing.get_args(parameter_type)

#         is_tuple_of_single_type = (len(tuple_elements_type) == 2) and (tuple_elements_type[1] == Ellipsis)

#         elements_obey_type = (
#             self.single_type_case(value, tuple_elements_type[0])
#             if is_tuple_of_single_type
#             else self.multi_type_case(value, tuple_elements_type)
#         )
#         return container_obeys_type and elements_obey_type

#     def generate_object(self, value: Any, parameter_type: Type) -> Any:
#         return tuple(value)


# class DictHandler(TypeHandler):
#     def does_type_match(self, value: Any, parameter_type: Type) -> bool:
#         container_obeys_type = isinstance(value, Dict)

#         key_elements_type, value_elements_type = typing.get_args(parameter_type)
#         key_elements_type_handler: TypeHandler = TYPE_HANDLER_REGISTER[key_elements_type]
#         value_elements_type_handler: TypeHandler = TYPE_HANDLER_REGISTER[value_elements_type]

#         keys_obey_type = all([do_the_types_match(element, key_elements_type) for element in value.keys()])
#         values_obey_type = all([do_the_types_match(element, value_elements_type) for element in value.values()])
#         return container_obeys_type and keys_obey_type and values_obey_type

#     def generate_object(self, value: Any, parameter_type: Type) -> Any:
#         ...


# TYPE_HANDLER_REGISTER: Dict[Type, TypeHandler] = {
#     int: PrimitiveTypeHandler(),
#     float: PrimitiveTypeHandler(),
#     str: PrimitiveTypeHandler(),
#     bool: PrimitiveTypeHandler(),
#     Any: AnyHandler(),
#     Union: UnionHandler(),
#     list: ListHandler(),
#     tuple: TupleHandler(),
# }


# class TypeHandlerRegister:
#     def __init__(self, type_handler_cls: Type[TypeHandler]) -> None:
#         self.type_handler_cls = type_handler_cls

#     def get(self, parameter_type: Type) -> TypeHandler:
#         ...

#     @classmethod
#     def register(cls, type_handler_cls: Type[TypeHandler]):
#         ...
