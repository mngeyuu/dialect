from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('', views.home, name='home'),  # Electron 健康检查 GET / 需返回 200
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('core/', views.home, name='home-legacy'),
]

# 开发环境提供媒体文件
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)