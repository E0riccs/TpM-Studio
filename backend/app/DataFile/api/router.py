from fastapi import APIRouter


from app.DataFile.api.v1.dFile import router as df_router

v1 = APIRouter()

v1.include_router(df_router)

