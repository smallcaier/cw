from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.authentication import BasicAuthentication
from app01 import models

ORDER_DICT = {
    1: {
        'name': '媳妇儿',
        'age': 18,
        'gender': '男',
        'content': '真漂亮'
    },
    2: {
        'name': '迪丽热巴',
        'age': 18,
        'gender': '充气',
        'content': '太漂亮了'
    }
}


def md5(user):
    import hashlib
    import time

    ctime = str(time.time())

    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    '''
    用户登录认证
    '''

    def post(self, request, *args, **kwargs):

        ret = {'code': 1000, 'msg': None}
        try:
            user = request.POST.get('username')
            pwd = request.POST.get('password')
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = '用户名或密码错误'
            # 为登陆用户创建token
            token = md5(user)
            ret['token'] = token
            # 存在就更新,不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = '请求异常'

        return JsonResponse(ret)


# class Authtication(object):
#
#     def authenticate(self, request):
#         token = request.GET.get('token')
#         token_obj = models.UserToken.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed('用户认证失败')
#         # 在framework内部会将两个字段赋值给request,以供后续使用
#         return (token_obj.user, token_obj)
#
#     def authenticate_header(self, request):  # 必须要有
#         pass


class OrderView(APIView):
    '''
    订单相关业务
    '''
    authentication_classes = []  # 应用自己写的认证,需要认证的类都要写

    def get(self, request, *args, **kwargs):
        # request.user   不同的用户
        # request.auth   用户信息
        ## 用户登录后携带着token就是说明在登录状态
        ## token = request.GET.get('token')
        ## if not token:
        ##     return HttpResponse('用户未登录')
        ret = {'code': 1000, 'msg': None, 'data': None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)

class UserInfoView(APIView):
    '''
    匿名用户
    '''
    def get(self,request,*args,**kwargs):
        print(request.user)

        return HttpResponse('用户信息')