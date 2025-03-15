from fastapi import Depends, Request, FastAPI, Form, status, Security, HTTPException, Response, Query, WebSocket, WebSocketDisconnect, APIRouter
from typing import Optional, List, Dict, Tuple
import asyncio
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import jwt
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, desc
from sqlalchemy.future import select
from db import (get_game, get_games, get_reviews, get_users, get_users_ratings, get_experts_ratings, get_profile_data,
                add_game, add_user, add_profile, add_review, update_review, update_profile, update_avg_users_rating,
                check_review, init_db)

templates = Jinja2Templates(directory='templates')
SECRET_KEY = 'REWSTRDYT$$^ueyvewuitfj()*#o239'

def get_current_user(request: Request):
    token = request.cookies.get('access_token')
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None

def get_token(username: str):
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {'sub': username, 'exp': expire}
    return {'access_token': jwt.encode(payload, SECRET_KEY, algorithm='HS256'), 'token_type': 'bearer'}