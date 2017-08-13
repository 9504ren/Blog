from django.shortcuts import render,HttpResponse,redirect
from ..form.account import LoginForm,LoginForm1
from repository import models
import json,time,random
# Create your views here.
def login(request):
    '''登录'''
    if request.method=='GET':
        return render(request,'login.html')
    elif request.method=='POST':
        msg={'status':False,'message':None,'data':None}
        form = LoginForm(request=request, data=request.POST)
        #from验证
        if form.is_valid():#通过了form验证
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('id', 'nickname',
                       'username', 'email',
                       'avatar',
                       ).first()#找出该用户名，密码的人
            if not user_info:
                msg['message'] = '用户名或密码错误'
            else:
                msg['status'] = True
                request.session['user_info'] = user_info
                print(request.session['user_info'])
                msg['data']=user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 7)
        else:
            if 'check_code' in form.errors:
                msg['message'] = '验证码错误或者过期'
            else:
                msg['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(msg))

def check(request):
    from io import BytesIO
    from utils.check_code import create_validate_code
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream,'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method=='GET':
        return render(request,'regist.html')
    elif request.method=='POST':
        msg = {'status': False, 'message': None, 'data': None}
        form = LoginForm1(request=request, data=request.POST)
        print(form)
        if form.is_valid():
            if form.cleaned_data.get('password1')==form.cleaned_data.get('password2'):
                username=form.cleaned_data.get('username')
                user_info = models.UserInfo.objects.filter(username=username).values().first()  # 找出该用户名，密码的人
                if user_info:
                    msg['message'] = '该用户名已存在'
                else:
                    password=form.cleaned_data.get('password1')
                    email=form.cleaned_data.get('email')
                    msg['status']=True
                    models.UserInfo.objects.create(username=username,password=password,email=email,create_time=time.time(),avatar='/',nickname=random.random())
                    user_info = models.UserInfo.objects. \
                        filter(username=username, password=password). \
                        values('id', 'nickname',
                               'username', 'email',
                               'avatar',
                               ).first()
                    request.session['user_info']=user_info
            else:
                msg['message'] = '密码不相等'
        else:
            if 'check_code' in form.errors:
                msg['message'] = '验证码错误或者过期'
            else:
                msg['message'] = '请完整填写'
        print(msg)
        return HttpResponse(json.dumps(msg))