
from rest_framework import viewsets
from resimyukle_rest.serializers import UploadImageSerializer
from resimyukle.models import Resim


class UploadImageViewSet(viewsets.ModelViewSet):
    queryset = Resim.objects.all()
    serializer_class = UploadImageSerializer
