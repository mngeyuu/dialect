import os
import sys
import tempfile
import logging
import shutil
import importlib.util


# 加载辅助函数
def load_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# 创建虚拟模块创建函数
def create_module_files(temp_dir):
    # Create appdirs
    appdirs_dir = os.path.join(temp_dir, "appdirs")
    os.makedirs(appdirs_dir, exist_ok=True)
    with open(os.path.join(appdirs_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("""
def user_data_dir(*args, **kwargs):
    import os
    return os.path.expanduser('~')
""")

    # Create django_filters
    filters_dir = os.path.join(temp_dir, "django_filters")
    os.makedirs(filters_dir, exist_ok=True)
    os.makedirs(os.path.join(filters_dir, "rest_framework"), exist_ok=True)

    with open(os.path.join(filters_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# django_filters\n")

    with open(os.path.join(filters_dir, "rest_framework", "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# django_filters.rest_framework\n")

    # Create corsheaders
    cors_dir = os.path.join(temp_dir, "corsheaders")
    os.makedirs(cors_dir, exist_ok=True)

    with open(os.path.join(cors_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# corsheaders\n")

    with open(os.path.join(cors_dir, "middleware.py"), "w", encoding="utf-8") as f:
        f.write("""
class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = '*'
        return response
""")

    # Create rest_framework
    rest_dir = os.path.join(temp_dir, "rest_framework")
    os.makedirs(rest_dir, exist_ok=True)

    with open(os.path.join(rest_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# rest_framework\n")

    with open(os.path.join(rest_dir, "viewsets.py"), "w", encoding="utf-8") as f:
        f.write("""
class ViewSet:
    pass

class ModelViewSet(ViewSet):
    pass
""")

    with open(os.path.join(rest_dir, "filters.py"), "w", encoding="utf-8") as f:
        f.write("""
class SearchFilter:
    pass

class OrderingFilter:
    pass
""")

    with open(os.path.join(rest_dir, "status.py"), "w", encoding="utf-8") as f:
        f.write("""
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
""")

    return temp_dir


# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

try:
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    logging.info(f"Created temp directory: {temp_dir}")

    # Create virtual modules
    create_module_files(temp_dir)
    logging.info("Created virtual modules")

    # Add to path
    sys.path.insert(0, temp_dir)

    # Setup backend path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        backend_dir = os.path.join(sys._MEIPASS, 'backend')

    logging.info(f"Backend directory: {backend_dir}")
    sys.path.insert(0, backend_dir)

    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dialect_search.settings')

    logging.info("Initializing Django...")
    import django

    django.setup()

    # Setup database path
    db_dir = os.path.join(os.environ.get('APPDATA', ''), 'dialect-app')
    os.makedirs(db_dir, exist_ok=True)

    from django.conf import settings

    if hasattr(settings, 'DATABASES') and 'default' in settings.DATABASES:
        if 'NAME' in settings.DATABASES['default']:
            db_path = os.path.join(db_dir, 'dialect.sqlite3')
            logging.info(f"Setting database path: {db_path}")
            settings.DATABASES['default']['NAME'] = db_path

    # Run server
    logging.info("Starting server...")
    from django.core.management import execute_from_command_line

    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])

except Exception as e:
    logging.error(f"Error: {str(e)}")
    import traceback

    logging.error(traceback.format_exc())
    sys.exit(1)
finally:
    if 'temp_dir' in locals():
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            logging.info(f"Cleaned up temp directory")
        except Exception as e:
            logging.error(f"Failed to clean up: {e}")