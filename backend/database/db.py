'''
数据库引入
'''
import sys
from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from backend.core.conf import settings
from backend.common.log import log
from backend.common.model import MappedBase



def create_db_link():
    '''
    创建数据库连接
    '''
    url = URL.create(
        drivername="sqlite+aiosqlite",
        database=settings.DATABASE_PATH       
    )
    
    return url


def create_db_session(url: str = "") -> sessionmaker:
    '''
    创建数据库会话
    '''
    engine =create_engine(url,echo=settings.DATABASE_ECHO)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal


def create_async_engine_and_session(url: str | URL) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """创建数据库引擎和 Session"""
    try:
        # 数据库引擎
        engine = create_async_engine(
            url,
            echo=settings.DATABASE_ECHO,
            echo_pool=settings.DATABASE_POOL_ECHO,
            future=True,
            # 中等并发
            pool_size=10,  # 低：- 高：+
            max_overflow=20,  # 低：- 高：+
            pool_timeout=30,  # 低：+ 高：-
            pool_recycle=3600,  # 低：+ 高：-
            pool_pre_ping=True,  # 低：False 高：True
            pool_use_lifo=False,  # 低：False 高：True
        )
        # log.success('数据库连接成功')
    except Exception as e:
        log.error('❌ 数据库链接失败 {}', e)
        sys.exit()
    else:
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session

async def get_db():
    """session 生成器"""
    async with async_db_session() as session:
        yield session


async def create_table() -> None:
    """创建数据库表"""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)

SQLALCHEMY_DATABASE_URL = create_db_link()

# 异步数据库引擎
async_engine, async_db_session = create_async_engine_and_session(SQLALCHEMY_DATABASE_URL)
CurrentSession = Annotated[AsyncSession, Depends(get_db)]





