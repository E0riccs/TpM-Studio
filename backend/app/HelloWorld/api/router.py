# -*- coding: utf-8 -*-

# 在app内引入api

from fastapi import APIRouter

from backend.app.HelloWorld.api.v1.helloworld import router as hello_router

v1 = APIRouter()

v1.include_router(hello_router)