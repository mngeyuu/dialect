import PyInstaller.__main__
import os
import sys
import shutil

# Project root directory
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

print("Starting Django packaging...")

# Create minimal server script
with open("server.py", "w", encoding="utf-8") as f:
    f.write("""
import os
import sys
import tempfile
import logging
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

try:
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    sys.path.insert(0, temp_dir)

    # Create backend path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if getattr(sys, 'frozen', False):
        backend_dir = os.path.join(sys._MEIPASS, 'backend')

    sys.path.insert(0, backend_dir)

    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dialect_search.settings')

    import django
    django.setup()

    # Run server
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '8000', '--noreload'])

except Exception as e:
    logging.error("Error: %s", str(e))
    import traceback
    logging.error(traceback.format_exc())
    sys.exit(1)
finally:
    if 'temp_dir' in locals():
        shutil.rmtree(temp_dir, ignore_errors=True)
""")

# PyInstaller command
pyinstaller_args = [
    "server.py",
    "--name=django-server",
    "--onefile",
    "--noconsole",
    f"--add-data={os.path.join(project_root, 'backend')}{os.pathsep}backend",
    "--hidden-import=django",
    "--hidden-import=rest_framework",
    "--hidden-import=django_filters",
    "--hidden-import=corsheaders"
]

# Run PyInstaller
print("Running PyInstaller...")
PyInstaller.__main__.run(pyinstaller_args)

# Cleanup
os.remove("server.py")

# Copy to resources
dist_file = os.path.join(project_root, "dist", "django-server.exe")
resources_dir = os.path.join(project_root, "resources")
os.makedirs(resources_dir, exist_ok=True)

target_path = os.path.join(resources_dir, "django-server.exe")
shutil.copy2(dist_file, target_path)

print(f"Django server packaged: {target_path}")