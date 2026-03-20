# run_server.py
import os
import sys
import django
from django.core.management import call_command
import signal
import threading
import time

# 设置Django环境
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'dialect_search.settings'  # 【需修改】替换为您的Django项目的settings模块路径
)  # 例如: 'dialect_project.settings'


def run_django():
    # 初始化Django
    django.setup()

    # 执行数据库迁移
    call_command('migrate')

    # 启动Django开发服务器
    call_command('runserver', '127.0.0.1:8000', '--noreload')


if __name__ == "__main__":
    # 在单独线程中启动Django
    django_thread = threading.Thread(target=run_django)
    django_thread.daemon = True
    django_thread.start()

    # 保持脚本运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)