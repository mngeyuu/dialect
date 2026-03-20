from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DialectWordViewSet, import_excel

router = DefaultRouter()
router.register(r'dialect-words', DialectWordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('import-excel/', import_excel, name='import-excel'),
]