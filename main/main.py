from imports import FastAPI, StaticFiles, init_db
from tops import router as tops_router
from reg_and_profile import router as reg_and_profile_router
from login_logout import router as login_logout_router
from admin import router as admin_router
from websocket import router as websocket_router, ConnectionManager
from game import router as game_router
from main_page_and_search import router as main_page_and_search_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(tops_router)
app.include_router(reg_and_profile_router)
app.include_router(login_logout_router)
app.include_router(admin_router)
app.include_router(websocket_router)
app.include_router(game_router)
app.include_router(main_page_and_search_router)

# @app.on_event("startup")
# async def on_startup():
#     await init_db()


