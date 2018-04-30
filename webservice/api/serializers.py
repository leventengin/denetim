from rest_framework import serializers
from ..models import BlogPost, MacPost, Memnuniyet


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



class MemnuniyetSerializer(serializers.ModelSerializer): # forms.ModelForm
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
