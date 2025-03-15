from imports import (APIRouter, Request, Optional, Security, get_current_user, Form, templates, RedirectResponse,
                     get_reviews, check_review, update_avg_users_rating, add_review, update_review, get_game)
from websocket import manager


router = APIRouter()

@router.api_route('/game/{id}', methods=['GET', 'POST'])
async def inspection_of_the_game(request: Request, id: int, review: str = Form(None), rating: int = Form(None), username: Optional[str] = Security(get_current_user)):
    try:
        reviews = await get_reviews(id)
        if request.method == 'POST':
            checked_review = await check_review(id, username)
            if not checked_review:
                avg_users_rating = 0
                for i in reviews:
                    avg_users_rating += i[4]
                avg_users_rating = round((avg_users_rating + int(rating)) / (len(reviews) + 1), 1)
                await update_avg_users_rating(avg_users_rating, id)
                await add_review(id, username, review, rating)
                response = RedirectResponse(url=f'/game/{id}', status_code=303)
                if username:
                    response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                        httponly=True, max_age=3600)
                return response
            else:
                avg_users_rating = 0
                for i in reviews:
                    if i[2] != username:
                        avg_users_rating += i[4]
                avg_users_rating = round((avg_users_rating + int(rating)) / (len(reviews)), 1)
                await update_avg_users_rating(avg_users_rating, id)
                await update_review(review, rating, id, username)
                response = RedirectResponse(url=f'/game/{id}', status_code=303)
                if username:
                    response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                        httponly=True, max_age=3600)
                return response
        game = await get_game(id)
        try:
            chat_history = manager.chat_history[str(id)]
        except:
            chat_history = list()
        response = templates.TemplateResponse("game.html",
                                              {'request': request, 'game': game, 'reviews': reviews, 'username': username, 'history': chat_history})
        if username:
            response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                httponly=True, max_age=3600)
        return response
    except Exception as e:
        return {'mess': e}