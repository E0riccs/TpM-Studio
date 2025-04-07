# -*- coding: utf-8 -*-
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from backend.common.model import Base, id_key

# ORM：对象-关系映射，一个表对应一个类，表的字段对应类的属性，表的记录对应类的实体对象 

class Hello(Base):
    __tablename__ = "hellos_table"

    # 主键，一个id_key类型的 Mapped 映射列
    # Mapped 在新版本的 sqlalchemy 中被推荐使用，而非传统的 Column
    # init=False 表示不初始化, 多用于主键
    # 类型： id_key
    id: Mapped[id_key] = mapped_column(init=False,primary_key=True)

    # 产生的随机数字
    a_number: Mapped[int] = mapped_column(nullable=False)

    # 字符串属性
    a_string: Mapped[str] = mapped_column(String(10), nullable=False)