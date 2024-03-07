from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from src.model.database import init_models, session_local
from src.routers import author, publication, source, feedback, user, admin, analysis, department, nioktr, rid, \
    dissertation
from src.routers.admin.service import service_create_admin

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback.router)
app.include_router(author.router)
app.include_router(publication.router)
app.include_router(source.router)
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(analysis.router)
app.include_router(department.router)
app.include_router(nioktr.router)
app.include_router(rid.router)
app.include_router(dissertation.router)


# @app.on_event("startup")
# async def startup_init_tables():
#     await init_models()
#     db = session_local()
#     await service_create_admin(db)
#     await db.close()


@app.get("/openapi.json", include_in_schema=False)
async def openapi():
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/docs", include_in_schema=False)
async def get_docs(request: Request):
    return get_swagger_ui_html(openapi_url=request.scope.get('root_path') + "/openapi.json", title="Swagger")
