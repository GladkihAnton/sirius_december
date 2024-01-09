from datetime import date
from decimal import Decimal
from typing import Any, Dict, List

from sqlalchemy.orm import class_mapper

from webapp.crud.utils.operations import ModelT


def serialize_instance(instance: ModelT) -> Dict[str, Any]:
    columns = {column.key: column.type.python_type for column in class_mapper(instance.__class__).columns}
    serialized_data = {}
    for column, col_type in columns.items():
        value = getattr(instance, column)
        if col_type == Decimal:
            serialized_data[column] = float(value) if value is not None else None
        elif col_type == date:
            serialized_data[column] = value.isoformat() if value is not None else None
        else:
            serialized_data[column] = value
    return serialized_data


def serialize_model(model: List[ModelT] | ModelT) -> List[Dict[str, Any]] | Dict[str, Any]:
    if isinstance(model, list):
        return [serialize_instance(instance) for instance in model]
    else:
        return serialize_instance(model)
