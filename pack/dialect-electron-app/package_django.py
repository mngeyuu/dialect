import PyInstaller.__main__
import os
import sys
import shutil
import subprocess

# 项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

print("=== Django 打包工具 ===")
print(f"项目根目录: {project_root}")

# 服务器脚本内容 - 避免使用三引号文档字符串
server_code = (
    "import os\n"
    "import sys\n"
    "import tempfile\n"
    "import logging\n"
    "import shutil\n"
    "import traceback\n\n"

    "# 设置日志\n"
    "logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')\n"
    "logger = logging.getLogger('django-server')\n\n"

    "try:\n"
    "    # 创建临时目录\n"
    "    temp_dir = tempfile.mkdtemp(prefix='django_modules_')\n"
    "    logger.info('创建临时目录: %s', temp_dir)\n\n"

    "    # 创建虚拟模块\n"
    "    # appdirs 模块\n"
    "    appdirs_dir = os.path.join(temp_dir, 'appdirs')\n"
    "    os.makedirs(appdirs_dir, exist_ok=True)\n"
    "    with open(os.path.join(appdirs_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('def user_data_dir(*args, **kwargs):\\n    import os\\n    return os.path.expanduser(\"~\")')\n\n"

    "    # django_filters 模块\n"
    "    filters_dir = os.path.join(temp_dir, 'django_filters')\n"
    "    os.makedirs(filters_dir, exist_ok=True)\n"
    "    \n"
    "    # django_filters/__init__.py\n"
    "    with open(os.path.join(filters_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# django_filters\\n\\nclass FilterSet:\\n    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):\\n        self.data = data\\n        self.queryset = queryset\\n        self.request = request\\n        self.prefix = prefix\\n    def filter_queryset(self, queryset):\\n        return queryset')\n"
    "    \n"
    "    # django_filters/rest_framework/__init__.py\n"
    "    rest_framework_dir = os.path.join(filters_dir, 'rest_framework')\n"
    "    os.makedirs(rest_framework_dir, exist_ok=True)\n"
    "    with open(os.path.join(rest_framework_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# django_filters.rest_framework\\n\\nfrom django_filters import FilterSet\\n\\nclass DjangoFilterBackend:\\n    def filter_queryset(self, request, queryset, view):\\n        filter_class = getattr(view, \"filter_class\", None)\\n        if filter_class is None:\\n            return queryset\\n        return filter_class(request.query_params, queryset=queryset, request=request).filter_queryset(queryset)\\n\\nclass FilterSet(FilterSet):\\n    pass')\n\n"

    "    # corsheaders 模块\n"
    "    cors_dir = os.path.join(temp_dir, 'corsheaders')\n"
    "    os.makedirs(cors_dir, exist_ok=True)\n"
    "    with open(os.path.join(cors_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# corsheaders')\n"
    "    with open(os.path.join(cors_dir, 'middleware.py'), 'w') as f:\n"
    "        f.write('class CorsMiddleware:\\n    def __init__(self, get_response):\\n        self.get_response = get_response\\n    def __call__(self, request):\\n        response = self.get_response(request)\\n        response[\"Access-Control-Allow-Origin\"] = \"*\"\\n        return response')\n\n"

    "    # rest_framework 模块\n"
    "    rest_dir = os.path.join(temp_dir, 'rest_framework')\n"
    "    os.makedirs(rest_dir, exist_ok=True)\n"
    "    \n"
    "    # __init__.py\n"
    "    with open(os.path.join(rest_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# rest_framework\\nfrom rest_framework.viewsets import *\\nfrom rest_framework.serializers import *\\nfrom rest_framework.views import *\\nfrom rest_framework.decorators import *\\nfrom rest_framework.response import *\\nfrom rest_framework.filters import *\\nfrom rest_framework.status import *\\nfrom rest_framework.routers import *')\n"

    "    # viewsets.py\n"
    "    with open(os.path.join(rest_dir, 'viewsets.py'), 'w') as f:\n"
    "        f.write('class ViewSet:\\n    pass\\n\\nclass ModelViewSet(ViewSet):\\n    pass\\n\\nclass ReadOnlyModelViewSet(ViewSet):\\n    pass')\n"

    "    # serializers.py\n"
    "    with open(os.path.join(rest_dir, 'serializers.py'), 'w') as f:\n"
    "        f.write('class Serializer:\\n    def __init__(self, *args, **kwargs):\\n        self.data = {}\\n\\nclass ModelSerializer(Serializer):\\n    pass')\n"

    "    # views.py\n"
    "    with open(os.path.join(rest_dir, 'views.py'), 'w') as f:\n"
    "        f.write('class APIView:\\n    pass')\n"

    "    # decorators.py\n"
    "    with open(os.path.join(rest_dir, 'decorators.py'), 'w') as f:\n"
    "        f.write('def api_view(methods):\\n    def decorator(func):\\n        return func\\n    return decorator\\n\\ndef action(methods=None, detail=False, **kwargs):\\n    def decorator(func):\\n        return func\\n    return decorator')\n"

    "    # filters.py\n"
    "    with open(os.path.join(rest_dir, 'filters.py'), 'w') as f:\n"
    "        f.write('class SearchFilter:\\n    pass\\n\\nclass OrderingFilter:\\n    pass')\n"

    "    # status.py\n"
    "    with open(os.path.join(rest_dir, 'status.py'), 'w') as f:\n"
    "        f.write('HTTP_200_OK = 200\\nHTTP_201_CREATED = 201\\nHTTP_400_BAD_REQUEST = 400\\nHTTP_404_NOT_FOUND = 404')\n"

    "    # response.py\n"
    "    with open(os.path.join(rest_dir, 'response.py'), 'w') as f:\n"
    "        f.write('class Response:\\n    def __init__(self, data=None, status=None, **kwargs):\\n        self.data = data\\n        self.status_code = status')\n"

    "    # fields.py\n"
    "    with open(os.path.join(rest_dir, 'fields.py'), 'w') as f:\n"
    "        f.write('class Field:\\n    pass\\n\\nclass CharField(Field):\\n    pass\\n\\nclass IntegerField(Field):\\n    pass')\n"

    "    # routers.py - 添加这个新模块\n"
    "    with open(os.path.join(rest_dir, 'routers.py'), 'w') as f:\n"
    "        f.write('class BaseRouter:\\n'\n"
    "                '    def __init__(self):\\n'\n"
    "                '        self.registry = []\\n\\n'\n"
    "                '    def register(self, prefix, viewset, basename=None, **kwargs):\\n'\n"
    "                '        self.registry.append((prefix, viewset, basename or prefix))\\n\\n'\n"
    "                '    def get_urls(self):\\n'\n"
    "                '        return []\\n\\n'\n"
    "                '    @property\\n'\n"
    "                '    def urls(self):\\n'\n"
    "                '        return self.get_urls()\\n\\n'\n"
    "                'class SimpleRouter(BaseRouter):\\n'\n"
    "                '    pass\\n\\n'\n"
    "                'class DefaultRouter(SimpleRouter):\\n'\n"
    "                '    def __init__(self, **kwargs):\\n'\n"
    "                '        super().__init__()\\n'\n"
    "                '        self._api_root_view = None\\n'\n"
    "                )\n"

    "    # pandas 模块\n"
    "    pandas_dir = os.path.join(temp_dir, 'pandas')\n"
    "    os.makedirs(pandas_dir, exist_ok=True)\n"
    "    \n"
    "    # pandas/__init__.py\n"
    "    with open(os.path.join(pandas_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# pandas mock implementation\\n\\n'\n"
    "                'class DataFrame:\\n'\n"
    "                '    def __init__(self, data=None, index=None, columns=None, dtype=None, copy=False):\\n'\n"
    "                '        self.data = data or {}\\n'\n"
    "                '        self.index = index\\n'\n"
    "                '        self.columns = columns\\n'\n"
    "                '        self.shape = (0, 0)\\n\\n'\n"
    "                '    def to_dict(self, orient=\"records\"):\\n'\n"
    "                '        return []\\n\\n'\n"
    "                '    def to_json(self, orient=\"records\"):\\n'\n"
    "                '        return \"[]\"\\n\\n'\n"
    "                '    def head(self, n=5):\\n'\n"
    "                '        return self\\n\\n'\n"
    "                '    def tail(self, n=5):\\n'\n"
    "                '        return self\\n\\n'\n"
    "                '    def __getitem__(self, key):\\n'\n"
    "                '        return self\\n\\n'\n"
    "                '    def __setitem__(self, key, value):\\n'\n"
    "                '        pass\\n\\n'\n"
    "                '    def __len__(self):\\n'\n"
    "                '        return 0\\n\\n'\n"
    "                'def read_excel(io, sheet_name=0, **kwargs):\\n'\n"
    "                '    return DataFrame()\\n\\n'\n"
    "                'def read_csv(filepath_or_buffer, **kwargs):\\n'\n"
    "                '    return DataFrame()\\n\\n'\n"
    "                'def concat(objs, **kwargs):\\n'\n"
    "                '    return DataFrame()\\n\\n'\n"
    "                'def Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False):\\n'\n"
    "                '    return []\\n\\n'\n"
    "                '# Define commonly used accessors\\n'\n"
    "                'NA = None\\n'\n"
    "                'NaT = None\\n'\n"
    "                'core = type(\"core\", (), {\"arrays\": type(\"arrays\", (), {})})\\n'\n"
    "                'io = type(\"io\", (), {})\\n'\n"
    "                )\n"

    "    # numpy 模块 (pandas依赖)\n"
    "    numpy_dir = os.path.join(temp_dir, 'numpy')\n"
    "    os.makedirs(numpy_dir, exist_ok=True)\n"
    "    with open(os.path.join(numpy_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# numpy mock\\n\\n'\n"
    "                'def array(object, dtype=None, **kwargs):\\n'\n"
    "                '    return object\\n\\n'\n"
    "                'def ndarray(shape, dtype=float, buffer=None, offset=0, strides=None, order=None):\\n'\n"
    "                '    return []\\n\\n'\n"
    "                'def zeros(shape, dtype=float):\\n'\n"
    "                '    return []\\n\\n'\n"
    "                'def ones(shape, dtype=float):\\n'\n"
    "                '    return []\\n\\n'\n"
    "                'int64 = int\\n'\n"
    "                'float64 = float\\n'\n"
    "                'bool_ = bool\\n'\n"
    "                'object_ = object\\n'\n"
    "                'nan = float(\"nan\")\\n'\n"
    "                )\n"

    "    # openpyxl 模块\n"
    "    openpyxl_dir = os.path.join(temp_dir, 'openpyxl')\n"
    "    os.makedirs(openpyxl_dir, exist_ok=True)\n"
    "    with open(os.path.join(openpyxl_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# openpyxl mock\\n\\ndef load_workbook(filename, **kwargs):\\n    class Workbook:\\n        def __init__(self):\\n            self.active = None\\n            self.sheetnames = []\\n        def close(self):\\n            pass\\n    return Workbook()')\n"

    "    # xlrd 模块\n"
    "    xlrd_dir = os.path.join(temp_dir, 'xlrd')\n"
    "    os.makedirs(xlrd_dir, exist_ok=True)\n"
    "    with open(os.path.join(xlrd_dir, '__init__.py'), 'w') as f:\n"
    "        f.write('# xlrd mock\\n\\ndef open_workbook(filename=None, **kwargs):\\n    class Book:\\n        def __init__(self):\\n            self.nsheets = 0\\n            self.sheet_names = []\\n        def sheet_by_index(self, index):\\n            class Sheet:\\n                def __init__(self):\\n                    self.nrows = 0\\n                    self.ncols = 0\\n                def row_values(self, rowx):\\n                    return []\\n            return Sheet()\\n    return Book()')\n"

    "    # 添加路径\n"
    "    sys.path.insert(0, temp_dir)\n"
    "    logger.info('添加临时目录到Python路径')\n\n"

    "    # 设置Django后端目录\n"
    "    backend_dir = os.path.dirname(os.path.abspath(__file__))\n"
    "    if getattr(sys, 'frozen', False):\n"
    "        backend_dir = os.path.join(sys._MEIPASS, 'backend')\n"
    "    sys.path.insert(0, backend_dir)\n"
    "    logger.info('后端目录: %s', backend_dir)\n\n"

    "    # 设置Django环境\n"
    "    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dialect_search.settings')\n"
    "    logger.info('初始化Django...')\n"
    "    import django\n"
    "    django.setup()\n\n"

    "    # 设置数据库路径\n"
    "    db_dir = os.path.join(os.environ.get('APPDATA', ''), 'dialect-app')\n"
    "    os.makedirs(db_dir, exist_ok=True)\n"
    "    from django.conf import settings\n"
    "    if hasattr(settings, 'DATABASES') and 'default' in settings.DATABASES:\n"
    "        if 'NAME' in settings.DATABASES['default']:\n"
    "            db_file = os.path.join(db_dir, 'dialect.sqlite3')\n"
    "            logger.info('设置数据库路径: %s', db_file)\n"
    "            settings.DATABASES['default']['NAME'] = db_file\n\n"

    "    # 启动服务器\n"
    "    logger.info('启动服务器...')\n"
    "    from django.core.management import execute_from_command_line\n"
    "    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])\n\n"

    "except Exception as e:\n"
    "    logger.error('启动失败: %s', str(e))\n"
    "    logger.error(traceback.format_exc())\n"
    "    sys.exit(1)\n"
    "finally:\n"
    "    # 清理临时目录\n"
    "    if 'temp_dir' in locals():\n"
    "        try:\n"
    "            shutil.rmtree(temp_dir, ignore_errors=True)\n"
    "            logger.info('清理临时目录')\n"
    "        except Exception as e:\n"
    "            logger.error('清理失败: %s', str(e))\n"
)

try:
    # 确保安装必要的依赖
    print("安装必要的依赖...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "django", "djangorestframework", "django-filter",
                               "django-cors-headers"], stdout=subprocess.DEVNULL)
        print("依赖安装完成")
    except Exception as e:
        print(f"安装依赖出错（可能已安装）: {e}")

    # 创建服务器脚本
    server_file = os.path.join(project_root, "django_server.py")
    print(f"创建服务器脚本: {server_file}")
    with open(server_file, "w", encoding="utf-8") as f:
        f.write(server_code)

    # PyInstaller命令行参数
    pyinstaller_args = [
        server_file,
        "--name=django-server",
        "--onefile",
        "--noconsole",
        f"--add-data={os.path.join(project_root, 'backend')}{os.pathsep}backend",
        # Django相关导入
        "--hidden-import=django",
        "--hidden-import=django.contrib",
        "--hidden-import=django.middleware",
        "--hidden-import=django.utils",
        "--hidden-import=django.db",
        # REST Framework相关导入
        "--hidden-import=rest_framework",
        "--hidden-import=rest_framework.viewsets",
        "--hidden-import=rest_framework.serializers",
        "--hidden-import=rest_framework.views",
        "--hidden-import=rest_framework.decorators",
        "--hidden-import=rest_framework.response",
        "--hidden-import=rest_framework.filters",
        "--hidden-import=rest_framework.status",
        "--hidden-import=rest_framework.fields",
        "--hidden-import=rest_framework.routers",  # 添加routers模块
        # Django Filter相关导入
        "--hidden-import=django_filters",
        "--hidden-import=django_filters.rest_framework",
        # CORS相关导入
        "--hidden-import=corsheaders",
        "--hidden-import=corsheaders.middleware",
        # 数据处理相关导入
        "--hidden-import=pandas",
        "--hidden-import=numpy",
        "--hidden-import=openpyxl",
        "--hidden-import=xlrd"
    ]

    # 运行 PyInstaller
    print("启动 PyInstaller 打包...")
    PyInstaller.__main__.run(pyinstaller_args)

    # 清理临时文件
    os.remove(server_file)
    print("临时文件已清理")

    # 复制到资源目录
    dist_file = os.path.join(project_root, "dist", "django-server.exe")
    resources_dir = os.path.join(project_root, "resources")
    os.makedirs(resources_dir, exist_ok=True)

    # 复制exe文件
    target_path = os.path.join(resources_dir, "django-server.exe")
    shutil.copy2(dist_file, target_path)

    print(f"Django服务器已打包: {target_path}")
    print("=== 打包完成 ===")

except Exception as e:
    print(f"打包过程出错: {e}")
    import traceback

    traceback.print_exc()