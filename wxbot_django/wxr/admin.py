from django.contrib import admin
from django.utils.html import format_html

from . import models as m
from functools import wraps
import wxr.filters


# Register your models here.

def long_text(func):
    @wraps(func)
    def wrapper(self, obj):
        max_lenth = 400
        text = func(self, obj)
        if text:
            text_brief = text if len(text) < max_lenth else text[:max_lenth] + '...'
        else:
            text_brief = ''

        return format_html('<span title="{}" style="word-break:break-all">{}</span>', text, text_brief)

    return wrapper


@admin.register(m.WxRaw)
class WxRawAdmin(admin.ModelAdmin):
    list_display = ['uin', 'created', 'req_url1', 'http_method', 'param1', 'content1']
    list_filter = ('http_method', wxr.filters.WxMsgCateFilter, 'uin')
    search_fields = ('req_url', 'param', 'content')

    @long_text
    def content1(self, obj):
        return obj.content

    content1.admin_order_field = 'content'

    @long_text
    def param1(self, obj):
        return obj.param

    param1.admin_order_field = 'param'

    @long_text
    def req_url1(self, obj):
        return obj.req_url

    req_url1.admin_order_field = 'req_url'


@admin.register(m.WxMsgHistory)
class WxMsgRecvHistoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in m.WxMsgHistory._meta.fields]


@admin.register(m.WxUser)
class WxUserAdmin(admin.ModelAdmin):
    list_display = [f.name for f in m.WxUser._meta.fields]


@admin.register(m.WxLoginHistory)
class WxLoginHistory(admin.ModelAdmin):
    change_list_template = 'wxr/WxLoginHistory/change_list.html'
    list_per_page = 10

    list_display = (
        'pk', 'qr_image', 'created', 'modified', 'uin', 'login_on', 'device_id', 'sid', 'skey', 'pass_ticket',
        'synckey')
    actions = ['kill_process', ]

    def qr_image(self, obj):
        return format_html('<img src="data:image/png;base64,{}" height=50px width=50px/>', obj.qr_image_base64)

    qr_image.admin_order_field = 'created'

    def kill_process(self, req, qs):
        from .views import processes
        killed_list = []
        for i in qs:
            pid = i.pid
            p = processes.get(pid)
            if p:
                killed_list.append(str(p.pid))
                p.terminate()
        if killed_list:
            self.message_user(req, '杀掉了：' + ','.join(killed_list))
        else:
            self.message_user(req, '没有活跃进程')
