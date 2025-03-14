from imports import APIRouter, Request, Optional, Security, get_current_user, Form, templates, RedirectResponse, status, add_game

router = APIRouter()

@router.get('/add_game_form')
async def add_game_form(request: Request, username: Optional[str] = Security(get_current_user)):
    response = templates.TemplateResponse('add_game.html', {'request': request, 'username': username})
    if username:
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                            httponly=True, max_age=3600)
    return response

@router.post('/add_game')
async def game_add(request: Request, img: str = Form(...), title: str = Form(...), description: str = Form(...), genre: str = Form(...), rating_igdb: float = Form(...),
                   trailer: str = Form(...), platforms: str = Form(...), avg_users_rating: float = 0, username: Optional[str] = Security(get_current_user)):
    try:
        if username == 'admin':
            await add_game(img, title, description, genre, rating_igdb, trailer, platforms, avg_users_rating)
        else:
            access_denied = 'ACCESS DENIED💀'
            response = templates.TemplateResponse('access_denied.html', {'request': request, 'access_denied': access_denied})
            if username:
                response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                    httponly=True, max_age=3600)
            return response
        response = RedirectResponse(url='/', status_code=303)
        if username:
            response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                httponly=True, max_age=3600)
        return response
    except Exception as e:
        return {'mess': e}