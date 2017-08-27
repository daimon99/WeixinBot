from fabric.operations import local
from fabric.api import lcd
import os

BASE_DIR = os.path.dirname(__file__)


def run_robot():
    """运行微信机器人"""
    with lcd(BASE_DIR):
        local('python3 -m robot.weixin')
