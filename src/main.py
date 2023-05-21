import time

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse

from auth.authentication import auth_router
from src.exceptions import StoryException
from src.models import users, articles
from src.db.database import engine
from src.routers.blogs import blog_router
from src.routers.articles import articles_router
from src.routers.files import files_router
from src.routers.products import products_router
from src.routers.templates import templates_router
from src.routers.users import users_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(blog_router)
app.include_router(users_router)
app.include_router(articles_router)
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(files_router)
app.include_router(templates_router)


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(status_code=418, content={"detail": exc.name})


# если нужно везде ошибки привести к одному формату
# @app.exception_handler(HTTPException)
# def custom_handler(request: Request, exc: StoryException):
#     return PlainTextResponse(str(exc), status_code=400)


users.Base.metadata.create_all(engine)
articles.Base.metadata.create_all(engine)


# можно задавать прослойки для разных действий, здесь например высчитывается время каждого запроса
@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response


origins = ["http://localhost:7000"]

# разрешение для взаимодействия с фронтом
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")
app.mount(
    "/templates/static", StaticFiles(directory="templates/static"), name="templates"
)
