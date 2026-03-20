
import os
import sys
import tempfile
import shutil
import traceback
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

try:
    # 创建临时目录
    temp_dir = tempfile.mkdtemp(prefix="django_tmp_")
    logger.info("创建临时目录: %s", temp_dir)

    # 创建虚拟模块
    # appdirs
    appdirs_dir = os.path.join(temp_dir, "appdirs")
    os.makedirs(appdirs_dir)
    
    with open(os.path.join(appdirs_dir, "__init__.py"), "w") as f:
        f.write("def user_data_dir(*args, **kwargs): return os.path.expanduser('~')")

    # django_filters
    filters_dir = os.path.join(temp_dir, "django_filters")
    os.makedirs(filters_dir)
    with open(os.path.join(filters_dir, "__init__.py"), "w") as f:
        f.write("# django_filters")

    # corsheaders
    cors_dir = os.path.join(temp_dir, "corsheaders")
    os.makedirs(cors_dir)
    with open(os.path.join(cors_dir, "__init__.py"), "w") as f:
        f.write("# corsheaders")
    with open(os.path.join(cors_dir, "middleware.py"), "w") as f:
        f.write("class CorsMiddleware: pass")

    # rest_framework
    rest_dir = os.path.join(temp_dir, "rest_framework")
    os.makedirs(rest_dir)
    with open(os.path.join(rest_dir, "__init__.py"), "w") as f:
        f.write("# rest_framework")
    with open(os.path.join(rest_dir, "viewsets.py"), "w") as f:
        f.write("class ViewSet: pass\nclass ModelViewSet(ViewSet): pass")
    with open(os.path.join(rest_dir, "filters.py"), "w") as f:
        f.write("class SearchFilter: pass\nclass OrderingFilter: pass")
    with open(os.path.join(rest_dir, "status.py"), "w") as f:
        f.write("HTTP_200_OK = 200\nHTTP_404_NOT_FOUND = 404")

    # 添加目录到路径
    sys.path.insert(0, temp_dir)

    # 设置后端目录
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        backend_dir = os.path.join(sys._MEIPASS, 'backend')

    sys.path.insert(0, backend_dir)

    # 尝试找到settings
    settings_module = 'dialect_search.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    # 初始化Django
    import django
    django.setup()

    # 启动服务器
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])

except Exception as e:
    logger.error("启动失败: %s", str(e))
    logger.error(traceback.format_exc())
    sys.exit(1)
finally:
    # 清理临时目录
    try:
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
    except:
        pass
