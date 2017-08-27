from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators import http
from . import models as m
# Create your views here.
from robot.dblog import get_login_id
from robot.weixin import WebWeixin
import logging
import sys


def start_wx(login_id):
    import logging.handlers
    import os.path

    LOG_DIR = os.path.dirname(os.path.dirname(__file__))
    os.makedirs(os.path.join(LOG_DIR, 'logs/'), exist_ok=True)

    wxlog = logging.handlers.WatchedFileHandler(os.path.join(LOG_DIR, 'logs/%s.log' % login_id))
    wxlog.setFormatter(
        logging.Formatter('%(asctime)s %(module)s:%(lineno)s[%(process)d] %(levelname)s %(message)s'))
    logging.root.handlers = [wxlog, ]
    logging.root.level = logging.INFO

    logging.info('#### START ####')
    logging.info('pid: %s', os.getpid())

    webwx = WebWeixin()
    webwx.autoReplyMode = True
    webwx.login_id = login_id
    webwx.silence = True
    webwx.start()


processes = {}


@http.require_http_methods(['POST'])
def wx_login_view(req):
    import multiprocessing
    login_id = get_login_id()
    process = multiprocessing.Process(target=start_wx, args=(login_id,))
    process.start()
    processes[process.pid] = process
    logging.info('process started: pid=%s', process.pid)
    return JsonResponse({'code': 0, 'login_id': login_id, 'msg': 'process started: pid=%s. total %s processes now.' % (
        process.pid, len(processes.keys()))})


@http.require_http_methods(['POST'])
def get_wx_login_qr_image(req: HttpRequest):
    login_id = req.POST.get('login_id')
    try:
        login = m.WxLoginHistory.objects.get(pk=login_id)
        if login.qr_image_base64:
            return JsonResponse({'code': 0, 'msg': 'ok', 'qr_base64': login.qr_image_base64})
        else:
            return JsonResponse({'code': -2, 'msg': '二维码图片不存在'})
    except m.WxLoginHistory.DoesNotExist:
        return JsonResponse({'code': -1, 'msg': 'login_id不存在'})


@http.require_http_methods(['POST'])
def check_login_result(req: HttpRequest):
    login_id = req.POST.get('login_id')
    try:
        login = m.WxLoginHistory.objects.get(pk=login_id)
        if login.uin:
            return JsonResponse({'code': 0, 'msg': 'login ok', 'uin': login.uin})
        else:
            return JsonResponse({'code': -2, 'msg': '没有结果'})
    except m.WxLoginHistory.DoesNotExist:
        return JsonResponse({'code': -1, 'msg': 'login_id不存在'})
