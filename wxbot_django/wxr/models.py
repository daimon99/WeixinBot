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
