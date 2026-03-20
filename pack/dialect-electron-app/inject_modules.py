import os
import sys
import tempfile
import shutil


def create_module_files(temp_dir):
    """Create module files in temp directory"""
    # Create appdirs
    appdirs_dir = os.path.join(temp_dir, "appdirs")
    os.makedirs(appdirs_dir, exist_ok=True)
    with open(os.path.join(appdirs_dir, "__init__.py"), "w") as f:
        f.write("""
def user_data_dir(*args, **kwargs):
    import os
    return os.path.expanduser('~')
""")

    # Create django_filters
    filters_dir = os.path.join(temp_dir, "django_filters")
    os.makedirs(filters_dir, exist_ok=True)
    os.makedirs(os.path.join(filters_dir, "rest_framework"), exist_ok=True)

    with open(os.path.join(filters_dir, "__init__.py"), "w") as f:
        f.write("# django_filters\n")

    with open(os.path.join(filters_dir, "rest_framework", "__init__.py"), "w") as f:
        f.write("# django_filters.rest_framework\n")

    # Create corsheaders
    cors_dir = os.path.join(temp_dir, "corsheaders")
    os.makedirs(cors_dir, exist_ok=True)

    with open(os.path.join(cors_dir, "__init__.py"), "w") as f:
        f.write("# corsheaders\n")

    with open(os.path.join(cors_dir, "middleware.py"), "w") as f:
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

    with open(os.path.join(rest_dir, "__init__.py"), "w") as f:
        f.write("# rest_framework\n")

    with open(os.path.join(rest_dir, "viewsets.py"), "w") as f:
        f.write("""
class ViewSet:
    pass

class ModelViewSet(ViewSet):
    pass
""")

    with open(os.path.join(rest_dir, "filters.py"), "w") as f:
        f.write("""
class SearchFilter:
    pass

class OrderingFilter:
    pass
""")

    with open(os.path.join(rest_dir, "status.py"), "w") as f:
        f.write("""
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
""")

    return temp_dir


# For testing
if __name__ == "__main__":
    temp = tempfile.mkdtemp()
    create_module_files(temp)
    print(f"Created modules in: {temp}")