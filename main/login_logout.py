from imports import APIRouter, HTMLResponse, Request, templates, Form, get_users, check_password_hash, get_token, RedirectResponse

router = APIRouter()

@router.get('/login_form', response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.post('/login')
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        users = await get_users()
        for i in users:
            if i['email'] == email and check_password_hash(i['password'], password):
                token = get_token(i['username'])
                response =  RedirectResponse(url='/', status_code=303)
                response.set_cookie(key='access_token', value=token['access_token'], httponly=True, max_age=3600)
                return response
        user_not_found = '⚠️ Користувача не знайдено. Перевірте введені дані'
        return templates.TemplateResponse('login.html', {'request': request, 'user_not_found': user_not_found})
    except Exception as e:
        return {'mess': e}

@router.get('/logout')
async def logout():
    try:
        response = RedirectResponse(url='/')
        response.delete_cookie('access_token')
        return response
    except Exception as e:
        return {'mess': e}