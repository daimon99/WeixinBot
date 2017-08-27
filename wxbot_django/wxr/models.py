from django.db import models
from django_extensions.db.models import TimeStampedModel


# Create your models here.

class WxRaw(TimeStampedModel):
    uin = models.CharField(blank=True, null=True, max_length=100)
    req_url = models.CharField(blank=True, null=True, max_length=500)
    http_method = models.CharField(max_length=10, blank=True, null=True)
    param = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)


class WxMsgHistory(TimeStampedModel):
    uin = models.CharField(blank=True, null=True, max_length=100)
    msg_cate = models.CharField(max_length=10, choices=(('recv', 'recv'), ('send', 'send')), blank=True, null=True,
                                help_text='消息种类，接收 or 发送')
    msg_type = models.CharField(max_length=50, help_text='消息类型，文本/语音...')
    from_user = models.CharField(max_length=100, blank=True, null=True)
    to_user = models.CharField(max_length=100, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    file_path = models.FilePathField(blank=True, null=True)

    from_user_name = models.CharField(max_length=200, blank=True, null=True)
    from_group_name = models.CharField(max_length=200, blank=True, null=True)
    to_user_name = models.CharField(max_length=200, blank=True, null=True)
    to_group_name = models.CharField(max_length=200, blank=True, null=True)


class WxUser(TimeStampedModel):
    uin = models.CharField(blank=True, null=True, max_length=128)
    username = models.CharField(blank=True, null=True, max_length=128)
    nick_name = models.CharField(blank=True, null=True, max_length=128)
    head_img_url = models.CharField(blank=True, null=True, max_length=1024)
    remark_name = models.CharField(blank=True, null=True, max_length=1024)
    sex = models.CharField(blank=True, null=True, max_length=2)
    signature = models.TextField(blank=True, null=True)

    last_login = models.DateTimeField(blank=True, null=True)
    login_total = models.IntegerField(default=0, help_text='累计登录次数')


class WxLoginHistory(TimeStampedModel):
    uin = models.CharField(blank=True, null=True, max_length=128)
    login_on = models.DateTimeField(blank=True, null=True)
    sid = models.CharField(blank=True, null=True, max_length=128)
    skey = models.CharField(blank=True, null=True, max_length=128)
    device_id = models.CharField(blank=True, null=True, max_length=128)
    pass_ticket = models.CharField(blank=True, null=True, max_length=128)
    cookie = models.TextField(blank=True, null=True)

    synckey = models.CharField(blank=True, null=True, max_length=128)

    qr_image_base64 = models.TextField(blank=True, null=True)

    pid = models.IntegerField(blank=True, null=True, help_text='监听的进程ID')
