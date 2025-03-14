from imports import APIRouter, HTMLResponse, Request, Optional, Security, get_current_user, Form, templates, get_games

router = APIRouter()

@router.get('/', response_class=HTMLResponse)
async def index(request: Request, username: Optional[str] = Security(get_current_user)):
    try:
        games = await get_games()
        response = templates.TemplateResponse("index.html", {'request': request, 'games': games, 'username': username})
        if username:
            response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                httponly=True, max_age=3600)
        return response
    except Exception as e:
        return {'mess': e}



@router.post('/search_results/')
async def search_results(request: Request, search: str = Form(None), username: Optional[str] = Security(get_current_user)):
    try:
        games = await get_games()
        list_of_searched_games = []
        for i in games:
            if search.lower() in i[2].lower():
                list_of_searched_games.append(i)
        response = templates.TemplateResponse('searched.html', {'request': request, 'searched': list_of_searched_games, 'username': username})
        if username:
            response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                httponly=True, max_age=3600)
        return response
    except Exception as e:
        return {'mess': e}