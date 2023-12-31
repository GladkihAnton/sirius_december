from typing import Any, Dict, List, Union

from sqlalchemy.orm import class_mapper

from webapp.crud.utils.operations import ModelT


def serialize_instance(instance: ModelT) -> Dict[str, Any]:
    columns = [column.key for column in class_mapper(instance.__class__).columns]
    return {column: getattr(instance, column) for column in columns}


def serialize_model(model: Union[List[ModelT], ModelT]) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    if isinstance(model, list):
        return [serialize_instance(instance) for instance in model]
    else:
        return serialize_instance(model)
