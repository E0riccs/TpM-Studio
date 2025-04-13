from fastapi import APIRouter

from app.HelloWorld.schemas.hello import GetHelloDetail,CreateHelloParam

from app.HelloWorld.services.hello_service import hello_service

from backend.common.response.response_schema import response_base,ResponseSchemaModel,ResponseModel

router = APIRouter()


@router.get("/", summary="Hello World")
async def hello():
    return {"Hello": "World"}

@router.get("/{name}", summary="Hello World")
async def hello_name(name: str) -> ResponseModel:
    return response_base.success(data={"Hello": name})

@router.get("/hello/{id}", summary="Complicate Hello World")
async def hello_num(id: int = 1) -> ResponseSchemaModel[GetHelloDetail]:
    '''
    隐式类型转换: FastAPI 通过 Pydantic 的 model_dump() 方法, 将数据模型 (转换为 dict) 转化为 schema 模型
    '''
    hello = await hello_service.get_hello(id)
    return response_base.success(data=hello)

@router.put("/hello", summary="Create a hello")
async def create_hello(param: CreateHelloParam) -> ResponseModel:
    await hello_service.create_hello(param)
    return response_base.success()