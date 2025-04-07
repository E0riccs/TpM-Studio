# -*- coding: utf-8 -*-
from datetime import datetime
from typing import BinaryIO, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.DataFile.models import DataFile
from backend.app.DataFile.utils import minio_client
from backend.common.log import log
from backend.utils.type_conversion import get_file_hash

class DataFileCRUD:
    """文件管理CRUD操作"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_file(
        self,
        file_obj: BinaryIO,
        filename: str,
        file_type: str,
        file_size: int,
        created_by: int,
        access_type: str = 'private',
        expiration_time: Optional[datetime] = None
    ) -> DataFile:
        """创建文件记录
        
        Args:
            file_obj: 文件对象
            filename: 文件名
            file_type: 文件类型
            file_size: 文件大小
            created_by: 创建者ID
            access_type: 访问类型
            expiration_time: 过期时间
            
        Returns:
            DataFile: 文件记录
        """
        try:
            # 计算文件哈希值
            file_hash = await get_file_hash(file_obj)
            
            # 生成存储路径
            object_name = f'{datetime.now().strftime("%Y%m%d")}/{file_hash}/{filename}'
            
            # 上传文件到MinIO
            upload_result = await minio_client.upload_file(
                file_obj=file_obj,
                object_name=object_name,
                content_type=file_type
            )
            
            # 创建文件记录
            file_record = DataFile(
                filename=filename,
                file_type=file_type,
                file_size=file_size,
                file_hash=file_hash,
                bucket_name=upload_result['bucket_name'],
                object_name=object_name,
                storage_path=f'{upload_result["bucket_name"]}/{object_name}',
                access_type=access_type,
                expiration_time=expiration_time,
                created_by=created_by
            )
            
            self.db.add(file_record)
            await self.db.commit()
            await self.db.refresh(file_record)
            
            return file_record
        except Exception as e:
            await self.db.rollback()
            log.error(f'文件创建失败: {str(e)}')
            raise
    
    async def get_file(
        self,
        file_id: int,
        generate_url: bool = False,
        url_expires: int = 3600
    ) -> tuple[DataFile, Optional[str]]:
        """获取文件信息
        
        Args:
            file_id: 文件ID
            generate_url: 是否生成访问URL
            url_expires: URL过期时间(秒)
            
        Returns:
            tuple: (文件记录, 访问URL)
        """
        query = select(DataFile).where(DataFile.id == file_id)
        result = await self.db.execute(query)
        file_record = result.scalar_one_or_none()
        
        if not file_record:
            return None, None
        
        if generate_url:
            url = await minio_client.get_file_url(
                object_name=file_record.object_name,
                expires=url_expires
            )
            return file_record, url
        
        return file_record, None
    
    async def download_file(self, file_id: int) -> tuple[BinaryIO, DataFile]:
        """下载文件
        
        Args:
            file_id: 文件ID
            
        Returns:
            tuple: (文件对象, 文件记录)
        """
        query = select(DataFile).where(DataFile.id == file_id)
        result = await self.db.execute(query)
        file_record = result.scalar_one_or_none()
        
        if not file_record:
            return None, None
        
        file_obj, _ = await minio_client.download_file(file_record.object_name)
        return file_obj, file_record
    
    async def delete_file(self, file_id: int) -> bool:
        """删除文件
        
        Args:
            file_id: 文件ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            query = select(DataFile).where(DataFile.id == file_id)
            result = await self.db.execute(query)
            file_record = result.scalar_one_or_none()
            
            if not file_record:
                return False
            
            # 删除MinIO中的文件
            await minio_client.delete_file(file_record.object_name)
            
            # 删除数据库记录
            await self.db.delete(file_record)
            await self.db.commit()
            
            return True
        except Exception as e:
            await self.db.rollback()
            log.error(f'文件删除失败: {str(e)}')
            raise