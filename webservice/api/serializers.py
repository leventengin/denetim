from rest_framework import serializers
from ..models import BlogPost, MacPost, Memnuniyet
from ..models import Operasyon_Data, Denetim_Data, Ariza_Data, rfid_dosyasi, yer_updown

class BlogPostSerializer(serializers.ModelSerializer): # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BlogPost
        fields = [
            'url',
            'id',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        read_only_fields = ['id', 'user']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value) # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used")
        return value



class MacPostSerializer(serializers.ModelSerializer): # forms.ModelForm
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = MacPost
        fields = [
            'url',
            'id',
            'mac_no',
            'timestamp',
        ]
        read_only_fields = ['id']

    # converts to JSON
    # validations for data passed

    def get_url(self, obj):
        # request
        request = self.context.get("request")
        return obj.get_api_url(request=request)

"""
    def create(self, validated_data):
        answer, created = MacPost.objects.update_or_create(
            question=validated_data.get('question', None),
            defaults={'answer': validated_data.get('answer', None)})
        return answer
"""


"""
    def validate_title(self, value):
        qs = MacPost.objects.filter(title__iexact=value) # including instance
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("This title has already been used")
        return value
"""



class MemnuniyetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Memnuniyet
        fields = [
            'url',
            'id',
            'tipi',
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
            'mac_no',
            'rfid_no',
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
            'yer',
            'proje',
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
