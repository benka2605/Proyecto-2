from rest_framework import serializers
from .models import *

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = '__all__'       

class PeriodistaSerializer(serializers.ModelSerializer):
    class Meta:         
        model = Periodista        
        fields = '__all__'




