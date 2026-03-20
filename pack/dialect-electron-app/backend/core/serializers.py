from rest_framework import serializers
from .models import DialectWord

class DialectWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DialectWord
        fields = '__all__'