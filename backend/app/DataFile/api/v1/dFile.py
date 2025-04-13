# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from backend.common.response.response_schema import response_base,ResponseSchemaModel,ResponseModel

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from backend.core.minio_conf import MinioSettings
from backend.database.db import CurrentSession
from backend.common.log import log

from backend.app.DataFile.services.Datafile_service import dataFileService

from backend.app.DataFile.schemas.MinioOperation import UploadOperaionDetail

router = APIRouter(prefix='/api/v1/files', tags=['文件管理'])

'''
note

解耦不完全，正在完成从这到service的转移
'''


@router.get("/health")
async def health_check() -> ResponseModel:
    if dataFileService.is_health():    
        return response_base.success()
    else:
        return response_base.error(msg="Storage unavailable")
    
    
@router.post('/upload')
async def upload_file(
    file: UploadFile = File(...),
    # access_type: str = Form('private'),
    # expiration_time: Optional[datetime] = Form(None),
    # db: CurrentSession = Depends()
) -> ResponseSchemaModel[UploadOperaionDetail]:
    """上传文件
    
    Args:
        file: 文件对象
        # access_type: 访问类型 (private/public-read)
        # expiration_time: 过期时间
        # db: 数据库会话
    """

    status = dataFileService.upload_file(file)
        
    return 


# @router.get('/info/{file_id}')
# async def get_file_info(
#     file_id: int,
#     generate_url: bool = False,
#     url_expires: int = 3600,
#     db: CurrentSession = Depends()
# ):
#     """获取文件信息
    
#     Args:
#         file_id: 文件ID
#         generate_url: 是否生成访问URL
#         url_expires: URL过期时间(秒)
#         db: 数据库会话
#     """
#     try:
#         crud = DataFileCRUD(db)
#         file_record, url = await crud.get_file(
#             file_id=file_id,
#             generate_url=generate_url,
#             url_expires=url_expires
#         )
        
#         if not file_record:
#             raise HTTPException(status_code=404, detail='文件不存在')
        
#         return {
#             'code': 200,
#             'message': '获取文件信息成功',
#             'data': {
#                 'file_id': file_record.id,
#                 'filename': file_record.filename,
#                 'file_type': file_record.file_type,
#                 'file_size': file_record.file_size,
#                 'access_type': file_record.access_type,
#                 'created_time': file_record.created_time,
#                 'download_url': url
#             }
#         }
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         log.error(f'获取文件信息失败: {str(e)}')
#         raise HTTPException(status_code=500, detail='获取文件信息失败')

@router.get('/download/{file_id}')
async def download_file(file_id: int, db: CurrentSession = Depends()):
    """下载文件
    
    Args:
        file_id: 文件ID
        db: 数据库会话
    """
    try:
        crud = DataFileCRUD(db)
        file_obj, file_record = await crud.download_file(file_id)
        
        if not file_obj or not file_record:
            raise HTTPException(status_code=404, detail='文件不存在')
        
        return StreamingResponse(
            content=file_obj,
            media_type=file_record.file_type,
            headers={
                'Content-Disposition': f'attachment; filename="{file_record.filename}"'
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error(f'文件下载失败: {str(e)}')
        raise HTTPException(status_code=500, detail='文件下载失败')

@router.delete('/{file_id}')
async def delete_file(file_id: int, db: CurrentSession = Depends()):
    """删除文件
    
    Args:
        file_id: 文件ID
        db: 数据库会话
    """
    try:
        crud = DataFileCRUD(db)
        success = await crud.delete_file(file_id)
        
        if not success:
            raise HTTPException(status_code=404, detail='文件不存在')
        
        return {
            'code': 200,
            'message': '文件删除成功'
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        log.error(f'文件删除失败: {str(e)}')
        raise HTTPException(status_code=500, detail='文件删除失败')