from rest_framework import serializers
from ..models import Memnuniyet, rfid_dosyasi, yer_updown
from ..models import Operasyon_Data, Denetim_Data, Ariza_Data, Sayi_Data
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')



class MemnuniyetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Memnuniyet
        fields = [
            'url',
            'id',
            'tipi',
            'proje',
            'p_alani',
            'yer',
            'mac_no',
            'oy',
            'sebep',
            'gelen_tarih',
            'timestamp',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)




class OperasyonSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Operasyon_Data
        fields = [
            'url',
            'id',
            'tipi',
            'proje',
            'p_alani',
            'yer',
            'mac_no',
            'rfid_no',
            'bas_tarih',
            'son_tarih',
            'bild_tipi',
            'timestamp',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)



class DenetimSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Denetim_Data
        fields = [
            'url',
            'id',
            'tipi',
            'proje',
            'p_alani',
            'yer',
            'mac_no',
            'rfid_no',
            'kod',
            'gelen_tarih',
            'timestamp',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)



class ArizaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Ariza_Data
        fields = [
            'url',
            'id',
            'tipi',
            'proje',
            'p_alani',
            'yer',
            'mac_no',
            'rfid_no',
            'rfid_kapat',
            'num',
            'sebep',
            'progress',
            'gelen_tarih',
            'timestamp',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class SayiSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Sayi_Data
        fields = [
            'url',
            'id',
            'tipi',
            'proje',
            'p_alani',
            'yer',
            'mac_no',
            'adet',
            'gelen_tarih',
            'timestamp',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class RfidSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = rfid_dosyasi
        fields = [
            'url',
            'id',
            'rfid_no',
            'proje',
            'rfid_tipi',
            'kullanici',
            'eleman',
            'adi',
            'soyadi',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)


class YerudSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = yer_updown
        fields = [
            'url',
            'id',
            'proje',
            'p_alani',
            'yer',
            'mac_no',
            'degis',
            'alive_time',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

