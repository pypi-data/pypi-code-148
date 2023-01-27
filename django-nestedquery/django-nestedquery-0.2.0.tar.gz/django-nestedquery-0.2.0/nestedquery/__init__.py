from __future__ import annotations

import uuid
from typing import List, Optional, Tuple, Type, Union

from django.db import DEFAULT_DB_ALIAS, models
from django.db.models import Field, Expression, QuerySet
from django.db.models.sql import datastructures


class VirtualTable(datastructures.BaseTable):
    def __init__(self, qs: QuerySet, alias: str):
        self.table_alias = alias
        self.qs = qs

    def as_sql(self, compiler, connection):
        base_sql, params = self.qs.query.sql_with_params()
        return f"({base_sql}) as {self.table_alias}", params

class Meta:
    app_label='django_nestedquery'

def VirtualModel(qs: QuerySet) -> Type[models.Model]:
    def field_from_col(
        col: List[Tuple[Expression, Tuple[str, List[Union[int, str]]], Optional[str]]]
    ) -> Field:
        field: Field
        try:
            field = col[0].target
        except AttributeError:
            field = col[0].output_field
        name = field.name
        if col[2] is not None:
            name = col[2]
        return name, field.clone()

    name = f"Virtual_{str(uuid.uuid4()).replace('-','_')}"
    compiler = qs.query.get_compiler(DEFAULT_DB_ALIAS)
    cols, _, _ = compiler.get_select()
    fields = dict(field_from_col(col) for col in cols)
    fields["__module__"] = __name__
    fields['Meta']=Meta

    cls = type(name, (models.Model,), fields)
    #remove the model from the app registry
    meta=cls._meta
    if meta.apps.all_models[meta.app_label][meta.model_name]==cls:
        del meta.apps.all_models[meta.app_label][meta.model_name]

    return cls


def NestedQuery(inner_qs: QuerySet) -> QuerySet:
    model = VirtualModel(inner_qs)
    qs = QuerySet(model)

    # set the alias to a node that generates the SQL rather than just the table name
    alias = qs.query.get_meta().db_table
    qs.query.alias_map[alias] = VirtualTable(inner_qs._clone(), alias)
    qs.query.alias_refcount[alias] = 1

    return qs
