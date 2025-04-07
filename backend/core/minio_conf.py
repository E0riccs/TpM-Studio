# -*- coding: utf-8 -*-
from typing import Literal

class MinioSettings:
    """MinIO配置"""
    
    # MinIO服务器配置
    MINIO_ENDPOINT: str = 'localhost:9000'
    MINIO_ACCESS_KEY: str = 'minioadmin'
    MINIO_SECRET_KEY: str = 'minioadmin'
    MINIO_SECURE: bool = False  # 是否使用HTTPS
    
    # 存储桶配置
    MINIO_BUCKET_NAME: str = 'tpm-studio'
    MINIO_BUCKET_POLICY: Literal['private', 'public-read', 'public-write'] = 'private'
    
    # 文件配置
    MINIO_MAX_FILE_SIZE: int = 1024 * 1024 * 800  # 最大文件大小(800MB)
    MINIO_ALLOWED_EXTENSIONS: list[str] = ['xls', 'xlsx','csv']