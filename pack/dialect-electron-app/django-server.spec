# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\pack\\dialect-electron-app\\django_server.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\pack\\dialect-electron-app\\backend', 'backend')],
    hiddenimports=['django', 'django.contrib', 'django.middleware', 'django.utils', 'django.db', 'rest_framework', 'rest_framework.viewsets', 'rest_framework.serializers', 'rest_framework.views', 'rest_framework.decorators', 'rest_framework.response', 'rest_framework.filters', 'rest_framework.status', 'rest_framework.fields', 'rest_framework.routers', 'django_filters', 'django_filters.rest_framework', 'corsheaders', 'corsheaders.middleware', 'pandas', 'numpy', 'openpyxl', 'xlrd'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='django-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
