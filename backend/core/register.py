from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.core.conf import settings
from backend.database.db import create_table
from backend.common.exception.exception_handler import register_exception


@asynccontextmanager
async def registre_init(app: FastAPI):
    """
    启动初始化

    :return:
    """
    # 创建数据库表
    await create_table()
    # # 连接 redis
    # await redis_client.open()
    # # 初始化 limiter
    # await FastAPILimiter.init(
    #     redis=redis_client,
    #     prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
    #     http_callback=http_limit_callback,
    # )

    yield
    '''
    yield 之前的代码, 会在线程开始时执行
    yield 之后的代码, 会在线程结束时执行
    '''

    # # 关闭 redis 连接
    # await redis_client.close()
    # # 关闭 limiter
    # await FastAPILimiter.close()

# app注册器
def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.PROJECT_NAME,
        lifespan=registre_init,
    )

    # socketio
    # register_socket_app(app)

    # # 日志
    # register_logger()

    # # 静态文件
    # register_static_file(app)

    # # 中间件
    # register_middleware(app)

    # 路由
    register_router(app)

    # # 分页
    # register_page(app)

    # 全局异常处理
    register_exception(app)

    return app

# 其他注册器……

# 路由注册器
def register_router(app: FastAPI):
    # 插件路由

    # 本体路由
    from backend.app.router import router
    app.include_router(router)

    # Extra
    # 确保路由名称唯一
    # 简化api名称