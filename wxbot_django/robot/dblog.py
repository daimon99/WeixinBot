# coding: utf8

import os
import django
import logging
import functools

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxbot_django.settings")
django.setup()

from wxr.models import WxRaw, WxMsgHistory


class decorator:
    @classmethod
    def ignore_error(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error('db save error')
                logging.exception(e)

        return wrapper


@decorator.ignore_error
def log_wx_raw(req_url=None, http_method='get', param=None, content=None, uin=None):
    WxRaw.objects.create(req_url=req_url, param=param, content=content, http_method=http_method, uin=uin)


@decorator.ignore_error
def log_wx_recv(from_user=None, to_user=None, msg=None, filepath=None, msg_type=None, uin=None):
    WxMsgHistory.objects.create(msg_cate='recv', from_user=from_user, to_user=to_user, msg=msg, filepath=filepath,
                                msg_type=msg_type, uin=uin)


@decorator.ignore_error
def log_wx_send(from_user=None, to_user=None, msg=None, filepath=None, msg_type=None, uin=None):
    WxMsgHistory.objects.create(msg_cate='send', from_user=from_user, to_user=to_user, msg=msg, filepath=filepath,
                                msg_type=msg_type, uin=uin)
