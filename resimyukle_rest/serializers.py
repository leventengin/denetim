
from rest_framework import serializers
from resimyukle.models import Resim


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resim
        fields = ('pk', 'kucuk_resim',)
