# -*- coding: utf-8 -*-
from app.HelloWorld.models.hello import Hello
from app.HelloWorld.schemas.hello import CreateHelloParam,UpdateHelloParam

from app.HelloWorld.cruds.hello_cruds import hello_dao

from backend.app.HelloWorld.models import hello
from backend.common.exception import errors

from database.db import async_db_session

import random

class HelloService():
    # 根据 id 获取 Hello
    @ staticmethod
    async def get_hello(hello_id:int) -> Hello:
        async with async_db_session() as db:
            hello = await hello_dao.get_hello(db, hello_id)
            if not hello:
                raise errors.NotFoundError(msg="Hello not found")

        return hello


    @ staticmethod
    async def create_hello(hello: CreateHelloParam) -> None:
        hello.a_number = random.randint(0, 100)

        async with async_db_session() as db:
            await hello_dao.create_hello(db, hello)

hello_service : HelloService = HelloService()