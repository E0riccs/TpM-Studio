# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Literal

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key

class DataFile(Base):
    """文件存储模型"""
    
    id: Mapped[id_key] = mapped_column(primary_key=True, init=False)
    
    # 文件基本信息
    filename: Mapped[str] = mapped_column(String(255), comment='文件名')
    file_type: Mapped[str] = mapped_column(String(50), comment='文件类型')
    file_size: Mapped[int] = mapped_column(comment='文件大小(字节)')
    file_hash: Mapped[str] = mapped_column(String(64), comment='文件哈希值')
    
    # MinIO存储信息
    bucket_name: Mapped[str] = mapped_column(String(100), comment='存储桶名称')
    object_name: Mapped[str] = mapped_column(String(255), comment='对象名称')
    storage_path: Mapped[str] = mapped_column(String(500), comment='存储路径')
    
    # 访问控制
    access_type: Mapped[str] = mapped_column(
        String(20),
        comment='访问类型',
        default='private'
    )
    expiration_time: Mapped[datetime | None] = mapped_column(
        comment='过期时间',
        default=None
    )
    
    # 文件状态
    status: Mapped[str] = mapped_column(
        String(20),
        comment='文件状态',
        default='active'
    )
    
    def __str__(self) -> str:
        return f'<DataFile {self.filename}>'