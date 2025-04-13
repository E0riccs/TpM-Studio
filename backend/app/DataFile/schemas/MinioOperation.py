from pydantic import ConfigDict
from datetime import datetime

from backend.common.schema import SchemaBase


class DataFileSchemaBase(SchemaBase):
    bucket_name: str
    object_name: str

# 响应模式
class UploadOperaionDetail(DataFileSchemaBase):
    upload_time: datetime | None = None

    version_id: str | None = None