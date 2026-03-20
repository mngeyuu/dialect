import sys
import os
import subprocess
import django
from django.core.management import call_command
import signal

# 设置Django环境

# 设置 Django 配置文件路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dialect_search.settings')

django.setup()

# 执行数据库迁移
call_command('migrate')

# 启动Django服务器
process = subprocess.Popen([
    sys.executable,
    'manage.py',
    'runserver',
    '127.0.0.1:8000'
])

# 处理应用退出
def cleanup(signum, frame):
    process.terminate()
    sys.exit(0)

signal.signal(signal.SIGTERM, cleanup)
signal.signal(signal.SIGINT, cleanup)

try:
    process.wait()
except KeyboardInterrupt:
    process.terminate()