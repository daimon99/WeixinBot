# coding: utf8
from django.contrib import admin
from django.db.models import Q


class WxMsgCateFilter(admin.SimpleListFilter):
    title = '消息种类'
    parameter_name = 'msg_cate'

    def lookups(self, request, model_admin):
        return (
            ('1', '登录消息'),
            ('2', '微信初始化消息'),
            ('3', '通讯录消息'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            q = Q(req_url__contains='webwxnewloginpage')
        elif self.value() == '2':
            q = Q(req_url__contains='webwxinit')
        elif self.value() == '3':
            q = Q(req_url__contains='webwxgetcontact') or Q(req_url__contains='webwxbatchgetcontact')
        else:
            q = Q()
        return queryset.filter(q)
