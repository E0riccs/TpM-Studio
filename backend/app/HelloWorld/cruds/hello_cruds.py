# -*- coding: utf-8 -*-
from app.HelloWorld.models.hello import Hello
from app.HelloWorld.schemas.hello import CreateHelloParam,UpdateHelloParam

from sqlalchemy import select, update

'''
在新版 sqlalchemy 中（1.4+），不再使用 query 等方法，改用 insert, update, delete, select 方法
'''

class HelloCRUD():
    # 根据 id 获取 Hello
    async def get_hello(self, db, hello_id:int) -> Hello | None:
        stmt = select(Hello).where(Hello.id == hello_id)
        hello = await db.execute(stmt)

        return hello.scalar()
    

    # 创建一个 Hello
    async def create_hello(self, db, param: CreateHelloParam) -> None:
        # new_hello = Hello(**param.model_dump())
        new_hello = Hello(
            a_number=param.a_number,
            a_string = param.a_string
        )

        db.add(new_hello)
        await db.commit()

        # 最佳实践
        # if flush:
        #     await session.flush()
        # if commit:
        #     await session.commit()


    # 更新一个 Hello
    async def update_hello(self, db, hello_id:int, param: UpdateHelloParam) -> int:
        update_data = param.model_dump(exclude_unset=True)

        stmt = update(Hello).where(Hello.id == hello_id).values(**update_data)
        result = await db.execute(stmt)
        await db.commit()

        # 返回受影响的行数
        return result.rowcount

hello_dao : HelloCRUD = HelloCRUD()