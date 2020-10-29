from django.db import models
from blueapps.account.models import User


class Role(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='角色名')
    permission = models.ManyToManyField('Permission',related_name="permission", verbose_name='权限')
    create_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="创建时间")
    is_delete = models.CharField(max_length=8, default=0, verbose_name='是否删除',help_text="0未删除,1已删除")
    menu = models.ManyToManyField("Menu",related_name="menu_role",verbose_name="菜单")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色'


class UserRole(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + self.role.name

    class Meta:
        verbose_name = '用户-角色关联'
        verbose_name_plural = '用户-角色关联'


class Permission(models.Model):
    app_id = models.CharField(max_length=128, verbose_name='应用id')
    url = models.CharField(max_length=128, verbose_name='权限路径')
    title = models.CharField(max_length=128, verbose_name='访问名称')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '权限'


class Menu(models.Model):
    name = models.CharField(max_length=128,null=True,blank=True,verbose_name="菜单名称")
    menu_parameter = models.CharField(max_length=2048,null=True,blank=True,verbose_name="详细参数")
    level = models.CharField(max_length=8,null=True,blank=True,verbose_name="菜单等级",help_text="1是一级,2是二级.以此类推")
    father_menu = models.CharField(max_length=8,null=True,blank=True,verbose_name="父级")
    create_time = models.DateTimeField(auto_now_add=True,null=True,blank=True,verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

