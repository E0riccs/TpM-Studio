#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import BinaryIO
import hashlib
from backend.common.enums import GenModelMySQLColumnType, GenModelPostgreSQLColumnType
from backend.core.conf import settings

async def get_file_hash(file_obj: BinaryIO) -> str:
    """计算文件的SHA-256哈希值
    
    Args:
        file_obj: 文件对象
        
    Returns:
        str: 文件的哈希值
    """
    sha256_hash = hashlib.sha256()
    
    # 保存当前文件指针位置
    current_position = file_obj.tell()
    
    # 重置文件指针到开始位置
    file_obj.seek(0)
    
    # 分块读取文件并更新哈希值
    chunk_size = 8192  # 8KB chunks
    while chunk := file_obj.read(chunk_size):
        sha256_hash.update(chunk)
    
    # 恢复文件指针位置
    file_obj.seek(current_position)
    
    return sha256_hash.hexdigest()


def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    Converts a sql type to a SQLAlchemy type.

    :param typing:
    :return:
    """
    if settings.DATABASE_TYPE == 'mysql':
        if typing in GenModelMySQLColumnType.get_member_keys():
            return typing
    else:
        if typing in GenModelPostgreSQLColumnType.get_member_keys():
            return typing
    return 'String'


def sql_type_to_pydantic(typing: str) -> str:
    """
    Converts a sql type to a pydantic type.

    :param typing:
    :return:
    """
    try:
        if settings.DATABASE_TYPE == 'mysql':
            return GenModelMySQLColumnType[typing].value
        else:
            if typing == 'CHARACTER VARYING':  # postgresql 中 DDL VARCHAR 的别名
                return 'str'
            return GenModelPostgreSQLColumnType[typing].value
    except KeyError:
        return 'str'
