# -*- coding: utf-8 -*-
from datetime import timedelta
from typing import BinaryIO, Optional

from minio import Minio
from minio.error import S3Error

from backend.core.minio_conf import MinioSettings
from backend.common.log import log

class MinioClient:
    """MinIO客户端管理类"""
    
    def __init__(self):
        self.client = Minio(
            endpoint=MinioSettings.MINIO_ENDPOINT,
            access_key=MinioSettings.MINIO_ACCESS_KEY,
            secret_key=MinioSettings.MINIO_SECRET_KEY,
            secure=MinioSettings.MINIO_SECURE
        )
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self) -> None:
        """确保存储桶存在"""
        try:
            if not self.client.bucket_exists(MinioSettings.MINIO_BUCKET_NAME):
                self.client.make_bucket(MinioSettings.MINIO_BUCKET_NAME)
                log.info(f'创建存储桶: {MinioSettings.MINIO_BUCKET_NAME}')
        except S3Error as e:
            log.error(f'存储桶操作失败: {str(e)}')
            raise
    
    async def upload_file(
        self,
        file_obj: BinaryIO,
        object_name: str,
        content_type: Optional[str] = None
    ) -> dict:
        """上传文件
        
        Args:
            file_obj: 文件对象
            object_name: 对象名称
            content_type: 内容类型
            
        Returns:
            dict: 上传结果
        """
        try:
            result = self.client.put_object(
                bucket_name=MinioSettings.MINIO_BUCKET_NAME,
                object_name=object_name,
                data=file_obj,
                length=-1,
                content_type=content_type
            )
            return {
                'bucket_name': result.bucket_name,
                'object_name': result.object_name,
                'version_id': result.version_id
            }
        except S3Error as e:
            log.error(f'文件上传失败: {str(e)}')
            raise
    
    async def download_file(self, object_name: str) -> tuple[BinaryIO, dict]:
        """下载文件
        
        Args:
            object_name: 对象名称
            
        Returns:
            tuple: (文件对象, 文件信息)
        """
        try:
            response = self.client.get_object(
                bucket_name=MinioSettings.MINIO_BUCKET_NAME,
                object_name=object_name
            )
            return response, response.stats
        except S3Error as e:
            log.error(f'文件下载失败: {str(e)}')
            raise
    
    async def delete_file(self, object_name: str) -> bool:
        """删除文件
        
        Args:
            object_name: 对象名称
            
        Returns:
            bool: 是否删除成功
        """
        try:
            self.client.remove_object(
                bucket_name=MinioSettings.MINIO_BUCKET_NAME,
                object_name=object_name
            )
            return True
        except S3Error as e:
            log.error(f'文件删除失败: {str(e)}')
            raise
    
    async def get_file_url(self, object_name: str, expires: int = 3600) -> str:
        """获取文件访问URL
        
        Args:
            object_name: 对象名称
            expires: 过期时间(秒)
            
        Returns:
            str: 文件访问URL
        """
        try:
            url = self.client.get_presigned_url(
                'GET',
                bucket_name=MinioSettings.MINIO_BUCKET_NAME,
                object_name=object_name,
                expires=timedelta(seconds=expires)
            )
            return url
        except S3Error as e:
            log.error(f'获取文件URL失败: {str(e)}')
            raise
