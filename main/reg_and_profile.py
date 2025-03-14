from imports import (APIRouter, HTMLResponse, Request, templates, Form, get_users, add_user, add_profile, get_token,
                     RedirectResponse, generate_password_hash, Optional, get_profile_data, update_profile, Security, get_current_user)

router = APIRouter()

@router.get('/registration_form', response_class=HTMLResponse)
async def registration_form(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})

@router.post('/registration')
async def registration(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        users = await get_users()
        for i in users:
            if username == i['username']:
                error_mess = f'⚠️ Користувач з іменем {i["username"]} вже існує'
                return templates.TemplateResponse("reg_error.html", {'request': request, 'error_mess': error_mess})
            elif email == i['email']:
                error_mess = f'⚠️ Пошта {i["email"]} вже зареєстрована'
                return templates.TemplateResponse("reg_error.html", {'request': request, 'error_mess': error_mess})
        await add_user(username, email, generate_password_hash(password))
        await add_profile(username)
        token = get_token(username)
        response = RedirectResponse(url='/', status_code=303)
        response.set_cookie(key='access_token', value=token['access_token'], httponly=True, max_age=3600)
        return response
    except Exception as e:
        return {'mess': e}

@router.api_route('/my_profile', methods=['GET', 'POST'])
async def profile(request: Request, username: Optional[str] = Security(get_current_user), name: Optional[str] = Form(None), age: Optional[str] = Form(None), country: Optional[str] = Form(None),
                       city: Optional[str] = Form(None), contacts: Optional[str] = Form(None), favourite_game: Optional[str] = Form(None)):
    profile = await get_profile_data(username)
    response = templates.TemplateResponse("profile.html", {'request': request, 'username': username, 'profile': profile})
    if request.method == 'POST':
        await update_profile(name, age, country, city, contacts, favourite_game, username)
        response = RedirectResponse(url='/my_profile', status_code=303)
        if username:
            response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                                httponly=True, max_age=3600)
        return response
    if username:
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                            httponly=True, max_age=3600)
    return response

@router.get('/profile_review/{user}')
async def profile_review(request: Request, user: str, username: Optional[str] = Security(get_current_user)):
    profile = await get_profile_data(user)
    response = templates.TemplateResponse("profile.html", {'request': request, 'username': username, 'profile': profile})
    if username:
        response.set_cookie(key="access_token", value=request.cookies.get("access_token"),
                            httponly=True, max_age=3600)
    return response