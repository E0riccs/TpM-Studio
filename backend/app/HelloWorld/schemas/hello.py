# -*- coding: utf-8 -*-
from pydantic import ConfigDict
from datetime import datetime

from backend.common.schema import SchemaBase
'''
继承BaseModel,帮助fastapi识别为body
'''


class HelloSchemaBase(SchemaBase):
    a_number: int | None = None
    a_string: str


class CreateHelloParam(HelloSchemaBase):
    pass

class UpdateHelloParam(HelloSchemaBase):
    pass


class GetHelloDetail(HelloSchemaBase):
    id: int

    created_time: datetime
    updated_time: datetime | None = None
