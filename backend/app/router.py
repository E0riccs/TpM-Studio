# -*- coding: utf-8 -*-

# 引入各个app的相应api
from fastapi import APIRouter

from backend.app.HelloWorld.api.router import v1 as HelloWorld_v1
from backend.app.DataFile.api.router import v1 as DataFile_v1

router = APIRouter()

router.include_router(HelloWorld_v1)
router.include_router(DataFile_v1)