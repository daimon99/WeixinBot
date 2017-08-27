# coding: utf8
import json
import pickle

import os
import django
import logging
import functools
from django.utils import timezone
import base64
from wxr.models import WxRaw, WxMsgHistory, WxUser, WxLoginHistory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wxbot_django.settings")
django.setup()


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


@decorator.ignore_error
def log_wx_user(user: dict):
    uin, username, nick_name, head_img_url, remark_name, sex, signature = (
        user.get('Uin'),
        user.get('UserName'),
        user.get('NickName'),
        user.get('HeadImgUrl'),
        user.get('RemarkName'),
        user.get('Sex'),
        user.get('Signature')
    )
    wx_user, is_created = WxUser.objects.get_or_create(uin=uin)

    wx_user.uin = uin
    wx_user.username = username
    wx_user.nick_name = nick_name
    wx_user.head_img_url = head_img_url
    wx_user.remark_name = remark_name
    wx_user.sex = sex
    wx_user.signature = signature

    wx_user.login_total += + 1
    wx_user.last_login = timezone.now()

    wx_user.save()


@decorator.ignore_error
def log_wx_login(login_id, uin, sid, skey, deviceId, pass_ticket, cookie):
    """
    self.uin, self.sid, self.skey, self.deviceId, self.pass_ticket     
    """
    cookie_txt = json.dumps(cookie.get_dict())
    WxLoginHistory.objects.filter(pk=login_id).update(
        uin=uin,
        sid=sid,
        skey=skey,
        device_id=deviceId,
        pass_ticket=pass_ticket,
        login_on=timezone.now(),
        cookie=cookie_txt
    )


@decorator.ignore_error
def log_wx_synckey(login_id, synckey):
    WxLoginHistory.objects.filter(pk=login_id).update(
        synckey=synckey
    )


@decorator.ignore_error
def log_wx_qr(login_id: int, pid: int, qr_bytes: bytes) -> int:
    qr_b64 = base64.b64encode(qr_bytes).decode('ascii')
    WxLoginHistory.objects.filter(pk=login_id).update(qr_image_base64=qr_b64, pid=pid)


def get_login_id():
    login = WxLoginHistory.objects.create()
    return login.pk
