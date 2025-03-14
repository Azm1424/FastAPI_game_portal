from imports import APIRouter, HTMLResponse, Request, templates, get_users_ratings, Optional, Security, get_current_user, get_experts_ratings

router = APIRouter()

@router.get('/top_10_users', response_class=HTMLResponse)
async def top_10_users(request: Request, username: Optional[str] = Security(get_current_user)):
    try:
        ratings = await get_users_ratings()
        ratings_lists = []
        count = 0
        for i in ratings:
            count += 1
            i = list(i)
            i.insert(0, count)
            ratings_lists.append(i)
        response = templates.TemplateResponse('top_10.html', {'request': request, 'ratings': ratings_lists, 'username': username})
        if username:
            response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                httponly=True, max_age=3600)
        return response
    except Exception as e:
        return {'mess': e}

@router.get('/top_10_experts', response_class=HTMLResponse)
async def top_10_experts(request: Request, username: Optional[str] = Security(get_current_user)):
    try:
        ratings = await get_experts_ratings()
        ratings_lists = []
        count = 0
        for i in ratings:
            count += 1
            i = list(i)
            i.insert(0, count)
            ratings_lists.append(i)
        response = templates.TemplateResponse('top_10.html', {'request': request, 'ratings':ratings_lists, 'username': username})
        if username:
            response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                httponly=True, max_age=3600)
        return response
    except Exception as e:
        return {'mess': e}