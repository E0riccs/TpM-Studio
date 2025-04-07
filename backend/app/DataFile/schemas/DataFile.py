from pydantic import ConfigDict
from datetime import datetime

from backend.common.schema import SchemaBase

class DataFileSchemaBase(SchemaBase):
    filename: str
    file_size: int
    file_hash: str
    file_root: str


class CreateDataFileParam(DataFileSchemaBase):
    pass

class UpdateDataFileParam(DataFileSchemaBase):
    pass


class GetDataFileDetail(DataFileSchemaBase):
    id: int

    file_type: str
    

    created_time: datetime
    updated_time: datetime | None = None