import json

from django.db.models import Q
from django.shortcuts import render

from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework.views import APIView

from blueapps.account.decorators import login_exempt
from .utils import MyPageNumberPagination
from .serializers import *
from .utils import get_object
from .models import *
from django.core import serializers
from . import models

def index(request):
    pass


# @method_decorator(login_exempt, name='dispatch')
# @method_decorator(csrf_exempt, name='dispatch')
class GetMenuListApi(APIView):

    def get(self, request, *args, **kwargs):
        menu_list = Menu.objects.all().order_by("-create_time")
        mypage = MyPageNumberPagination()
        page_query = mypage.paginate_queryset(queryset=menu_list, request=request, view=self)
        menuserializers = MenuSerializers(instance=page_query, many=True)
        return mypage.get_paginated_response(menuserializers.data)


@method_decorator(login_exempt, name='dispatch')
class AddMenuApi(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            Menu.objects.create(**data)
        except Exception as e:
            print(e)
            return JsonResponse({"code": 1, "message": "添加失败"})
        return JsonResponse({"code": 0, "message": "添加成功"})


@method_decorator(login_exempt, name='dispatch')
class UpdateMenuApi(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        menu_id = request.data.get("id")
        if not menu_id:
            return JsonResponse({"code": 1, "message": "缺少菜单id"})

        menu = Menu.objects.get(id=menu_id)
        menuser = MenuSerializers(instance=menu, data=data)
        if menuser.is_valid():
            menuser.save()
            return JsonResponse({"code": 0, "message": "修改成功"})
        else:
            return JsonResponse({"code": 1, "message": "参数不合法"})


@method_decorator(login_exempt, name='dispatch')
class DeleteMenuApi(APIView):

    def post(self, request, *args, **kwargs):
        menu_id = request.data.get("id")
        if not menu_id:
            return JsonResponse({"code": 1, "message": "缺少菜单id"})
        menu = get_object(Menu, menu_id)
        if not menu:
            return JsonResponse({"code": 1, "message": "未找到数据"})
        menu.delete()
        return JsonResponse({"code": 0, "message": "删除成功"})


@method_decorator(login_exempt, name='dispatch')
class GetRoleApi(APIView):

    def get(self, request, *args, **kwargs):
        roles = Role.objects.all().order_by("-create_time").filter(is_delete=0)
        mypage = MyPageNumberPagination()
        page_query = mypage.paginate_queryset(queryset=roles, request=request, view=self)
        roleserializers = RoleSerializers(instance=page_query, many=True)
        return mypage.get_paginated_response(roleserializers.data)


@method_decorator(login_exempt, name='dispatch')
class AddOrupdateRoleApi(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        permission_id_list = data.pop("permission_id_list")
        permissionobj_list = Permission.objects.filter(id__in=permission_id_list)
        if not permission_id_list:
            return JsonResponse({"code": 1, "message": "权限列表为空"})
        role_name = data.get("name")
        if not role_name:
            return JsonResponse({"code": 1, "message": "角色参数错误"})
        try:
            role = Role.objects.get(name=role_name)
        except Exception as e:
            role = Role.objects.create(**data)
        role.permission.set(*[permissionobj_list])
        role.save()
        return JsonResponse({"code": 0, "message": "添加成功"})


@method_decorator(login_exempt, name='dispatch')
class DeleteRoleApi(APIView):

    def post(self, request, *args, **kwargs):
        role_id = request.data.get("id")
        if not role_id:
            return JsonResponse({"code": 1, "message": "参数不正确"})
        Role.objects.filter(id=role_id).update(is_delete=1)
        return JsonResponse({"code": 0, "message": "删除成功"})




def list_permissions(request):
    permissions = serializers.serialize('json', models.Permission.objects.all())
    return JsonResponse({'permissions': permissions})


def add_permission(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        title = response.get('title')
        app_id = response.get('app_id')
        url = response.get('url')

        permission = models.Permission.objects.filter(url=url)
        if permission:
            message = '该访问权限路径{}已经存在'.format(permission.first())
            return JsonResponse({'message': message})
        per = models.Permission()
        per.url = url
        per.title = title
        per.app_id = app_id
        per.save()
        message = '权限{}添加成功'.format(permission.first())
    else:
        message = '没有添加权限'
    return JsonResponse({'message': message})


def update_permission(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        title = response.get('title')
        app_id = response.get('app_id')
        url = response.get('url')
        permission = models.Permission.objects.filter(url=url).first()
        if not permission:
            return JsonResponse({'message': '没有改访问权限路径，请重新填写'})
        if app_id:
            permission.app_id = app_id
        if title:
            permission.title = title
        permission.save()
        return JsonResponse({'message': '改访问权限路径{}修改成功'.format(permission)})


def del_permission(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        urls = response.get('url', [])
        models.Permission.objects.filter(url__in=urls).delete()
        return JsonResponse({'message': '访问权限路径{}已经删除'.format(urls)})
    else:
        return JsonResponse({'message': '此删除操作POST请求，请慎重！'})


def query_permission(request):
    url = request.GET.get('url')
    app_id = request.GET.get('app_id')
    user = request.user
    permission = models.Permission.objects.filter(app_id=app_id, url=url).first()
    if not permission:
        return JsonResponse({'message': '没有该访问权限路径', 'status': '0'})
    user = models.User.objects.filter(username=user).first()
    roles = user.userrole_set.all()
    permission_list = []
    for r in roles:
        pers = r.role.permission.all()
        permission_list.extend(pers)
    if permission in permission_list:
        return JsonResponse({'message': '当前用户拥有该访问权限', 'status': '1'})
    else:
        return JsonResponse({'message': '当前用户没有有该访问权限', 'status': '2'})


def query_user_permissions(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(username=username).first()
    if not user:
        return JsonResponse({'message': '没有该用户', 'status': '0'})
    roles = user.userrole_set.all()
    permission_list = []
    for r in roles:
        pers = r.role.permission.all()
        for p in pers:
            permission_list.append(p.url)
    permission_list = list(set(permission_list))
    return JsonResponse({'message': permission_list, 'status': '1'})

@method_decorator(login_exempt, name='dispatch')
class GetUserRoleApi(APIView):

    def get(self,request,*args,**kwargs):
        username = request.GET.get("username","")
        userrolelist = UserRole.objects.filter(user__username__contains=username).order_by("-c_time")
        mypage = MyPageNumberPagination()
        page_query = mypage.paginate_queryset(queryset=userrolelist,request=request,view=self)

        userrolelistser = UserRoleSerializers(instance=page_query,many=True)
        return mypage.get_paginated_response(userrolelistser.data)

@method_decorator(login_exempt, name='dispatch')
class AddUserRoleApi(APIView):

    def post(self, request, *args, **kwargs):
        user_id = request.data.get("user_id","")
        role_id = request.data.get("role_id","")
        if not user_id or not role_id:
            return JsonResponse({"code": 1, "message": "参数不正确"})
        try:
            hasuserrole = UserRole.objects.get(user_id=user_id,role_id=role_id)
        except Exception as e:
            hasuserrole = ""
        print(hasuserrole)
        if hasuserrole:
            return JsonResponse({"code": 1, "message": "用户已存在这个角色"})
        user = get_object(User,user_id)

        role = get_object(Role,role_id)
        if not user or not role:
            return JsonResponse({"code": 1, "message": "没有此用户或角色"})
        user_role = UserRole()
        user_role.user = user
        user_role.role = role
        user_role.save()
        return JsonResponse({"code": 0, "message": "添加成功"})

@method_decorator(login_exempt, name='dispatch')
class UpdateUserRoleApi(APIView):

    def post(self, request, *args, **kwargs):
        user_role_id = request.data.get("user_role_id", "")
        user_id = request.data.get("user_id","")
        role_id = request.data.get("role_id","")
        if not user_id or not role_id or not user_role_id:
            return JsonResponse({"code": 1, "message": "参数不正确"})
        try:
            hasuserrole = UserRole.objects.get(user_id=user_id,role_id=role_id)
        except Exception as e:
            hasuserrole = ""
        if hasuserrole:
            return JsonResponse({"code": 1, "message": "用户已存在这个角色"})
        role = get_object(Role,role_id)
        if not role:
            return JsonResponse({"code": 1, "message": "没有此用户或角色"})
        user_role = UserRole.objects.get(id = user_role_id)
        user_role.role = role
        user_role.save()
        return JsonResponse({"code": 0, "message": "添加成功"})

@method_decorator(login_exempt, name='dispatch')
class DeleteUserRoleApi(APIView):

    def post(self, request, *args, **kwargs):
        user_role_id = request.data.get("user_role_id", "")
        if not user_role_id:
            return JsonResponse({"code": 1, "message": "参数不正确"})
        try:
            user_role = UserRole.objects.get(id = user_role_id)
        except Exception as e:
            user_role = ""
        if not user_role:
            return JsonResponse({"code": 1, "message": "没有这条数据"})
        user_role.delete()
        return JsonResponse({"code": 0, "message": "添加成功"})