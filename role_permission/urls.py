from django.urls import path
from . import views

app_name = 'role_permission'
urlpatterns = [
    path('', views.index, name='index'),
    # 页面菜单接口
    path('addMenu', views.AddMenuApi.as_view(), name="add_menu"),
    path('getMenu', views.GetMenuListApi.as_view(), name="get_menu"),
    path('updateMenu', views.UpdateMenuApi.as_view(), name="update_menu"),
    path('deleteMenu', views.DeleteMenuApi.as_view(), name="delete_menu"),
    # 角色权限
    path('getRole', views.GetRoleApi.as_view(), name="get_role"),
    path('addOrUpdateRole', views.AddOrupdateRoleApi.as_view(), name="add_or_update_role"),
    path('deleteRole', views.DeleteRoleApi.as_view(), name="delete_role"),

    path('list/permissions/', views.list_permissions, name='list_permissions'),
    path('add/permission/', views.add_permission, name='add_permission'),
    path('update/permission/', views.update_permission, name='update_permission'),
    path('del/permission/', views.del_permission, name='del_permission'),
    path('query/permission/', views.query_permission, name='query_permission'),
    path('query/user/permissions/', views.query_user_permissions, name='query_user_permissions')

]
