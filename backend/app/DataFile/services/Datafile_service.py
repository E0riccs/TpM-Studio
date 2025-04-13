# -*- coding: utf-8 -*-

from fastapi import Depends, UploadFile

from backend.app.DataFile.utils.minio_client import minio_client

from backend.common.exception import errors
from backend.common.response.response_schema import response_base

from backend.app.DataFile.schemas.MinioOperation import UploadOperaionDetail


class DataFileService():
    # 检查
    @staticmethod
    def is_health(minio):
        try:
            if not minio.bucket_exists("your_bucket"):
                raise errors.ServerError(msg="Storage unavailable")
            return True
        except S3Error:
            raise errors.ServerError(msg="Storage unavailable")
        
    # 上传文件
    @staticmethod
    async def upload_file(
        file: UploadFile ,
        # access_type: str = 'private'
    ) -> UploadOperaionDetail:
        """
        上传文件

        :param file:
        :param access_type:
        :return:
        """


        # 验证文件大小
        file_size = file.size
        if file_size > minio_client.max_file_size:
            return response_base.fail(res=StandardResponseCode.HTTP_413,data=)

        try:
            # 重置文件指针
            await file.seek(0)
            
            # 验证文件类型
            file_ext = file.filename.split('.')[-1].lower()
            if file_ext not in minio_client.allowed_file_extension:
                raise errors.RequestError(msg='不支持的文件类型')
            
            # 上传文件
            status = await minio_client.upload_file(file, access_type, expiration_time)
            
            # 创建文件记录
            # crud = DataFileCRUD(db)
            #     file_record = await crud.create_file(
            #     file_obj=file.file,
            #     filename=file.filename,
            #     file_type=file.content_type,
            #     file_size=file_size,
            #     created_by=1,  # TODO: 从认证中获取用户ID
            #     access_type=access_type,
            #     expiration_time=expiration_time
            # )

            return status

        except HTTPException as e:
            raise e
        except Exception as e:
            log.error(f'文件上传失败: {str(e)}')
            raise HTTPException(status_code=500, detail='文件上传失败')


        
    
    # 下载文件


    # 删除文件


    # 调用其他服务，生成文件

dataFileService : DataFileService = DataFileService()