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
    hello = await hello_service.get_hello(id)
    return response_base.success(data=hello)

@router.put("/hello", summary="Create a hello")
async def create_hello(param: CreateHelloParam) -> ResponseModel:
    await hello_service.create_hello(param)
    return response_base.success()