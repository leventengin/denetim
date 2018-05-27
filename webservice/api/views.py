# generic
from django.db import models
from django.db.models import Q
from rest_framework import generics, mixins
from django.views.decorators.csrf import csrf_exempt
from ..models import BlogPost, MacPost, Memnuniyet
from ..models import Operasyon_Data, Denetim_Data, Ariza_Data, rfid_dosyasi, yer_updown
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer, MacPostSerializer, MemnuniyetSerializer
from .serializers import OperasyonSerializer, DenetimSerializer, ArizaSerializer, RfidSerializer, YerudSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, Http404


class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = BlogPostSerializer
    #queryset                = BlogPost.objects.all()

    @csrf_exempt
    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)
                    ).distinct()
        return qs

    @csrf_exempt
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}




class BlogPostDestroyView(mixins.DestroyModelMixin,  generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = BlogPostSerializer


    @csrf_exempt
    def get_queryset(self):
        qs = Blogpost.objects.get(pk=id)
        return qs

    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    @csrf_exempt
    def perform_delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class BlogPostDetailView(APIView):
    def get(self, request, pk):
        blogpost = get_object_or_404(BlogPost, pk=pk)
        serializer = BlogPostSerializer(blogpost)
        return Response(serializer.data)

    def delete(self, request, pk):
        blogpost = get_object_or_404(BlogPost, pk=pk)
        blogpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = BlogPostSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return BlogPost.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}



#----------------------------------------------------------------------------------------------


class MacPostRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = MacPostSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return MacPost.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class MacPostDetailView(APIView):
    def get(self, request, pk):
        macpost = get_object_or_404(MacPost, pk=pk)
        serializer = MacPostSerializer(macpost)
        return Response(serializer.data)

    def delete(self, request, pk):
        macpost = get_object_or_404(MacPost, pk=pk)
        macpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class MacList(APIView):
    """
    List all MacPost, or create a new MacPost.
    """
    def get(self, request, format=None):
        macpost = MacPost.objects.all()
        serializer = MacPostSerializer(macpost, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MacPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Mac_Bul(APIView):
    """
    find id from mac_no.
    """
    def get(self, request, format=None):
        deger = 52812233799999999
        print("find object çalıştı..mac bul  api içinden ....", deger)
        macpost = MacPost.objects.filter(mac_no=deger).first()
        print("macpost filter sonucu...", macpost)
        serializer = MacPostSerializer(macpost, many=True)
        return Response(serializer.data)

class Mac_Filter(generics.ListAPIView):
    serializer_class = MacPostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        mac_no = self.kwargs['mac_no']
        print(" get query set içinden  mac no...", mac_no)
        macpost = MacPost.objects.filter(mac_no=mac_no)
        print("filtrelenen obje...", macpost)
        return macpost
        #serializer = MacPostSerializer(macpost, many=True)
        #return Response(serializer.data)


class Mac_Query(generics.ListAPIView):
    serializer_class = MacPostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the mac list (actually must be one)
        for mac_no....
        """
        queryset = MacPost.objects.all()
        mac_no = self.request.query_params.get('mac_no', None)
        if mac_no is not None:
            queryset = queryset.filter(mac_no=mac_no)
        return queryset


class MacDetail(APIView):
    """
    Retrieve, update or delete a MacPost instance.
    """
    def get_object(self, pk):
        try:
            return MacPost.objects.get(pk=pk)
        except MacPost.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        macpost = self.get_object(pk)
        serializer = MacPostSerializer(macpost)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        macpost = self.get_object(pk)
        print("def - put içinden macpost objesi...", macpost)
        serializer = MacPostSerializer(macpost, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        macpost = self.get_object(pk)
        macpost.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------------------------

class MemnuniyetRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = MemnuniyetSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return Memnuniyet.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class MemnuniyetDetailView(APIView):
    def get(self, request, pk):
        memnuniyet = get_object_or_404(Memnuniyet, pk=pk)
        serializer = MemnuniyetSerializer(memnuniyet)
        return Response(serializer.data)

    def delete(self, request, pk):
        memnuniyet = get_object_or_404(Memnuniyet, pk=pk)
        memnuniyet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class MemnuniyetList(APIView):
    """
    List all Memnuniyet  (get), or create a new Memnuniyet (post).
    """
    def get(self, request, format=None):
        memnuniyet = Memnuniyet.objects.all()
        serializer = MemnuniyetSerializer(memnuniyet, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MemnuniyetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemnuniyetBul(APIView):
    """
    find id from mac_no.
    """
    def get(self, request, format=None):
        deger = 52812233799999999
        print("find object çalıştı..mac bul  api içinden ....", deger)
        memnuniyet = Memnuniyet.objects.filter(mac_no=deger).first()
        print("memnuniyet mac.. filter sonucu...", memnuniyet)
        serializer = MemnuniyetSerializer(memnuniyet, many=True)
        return Response(serializer.data)

class MemnuniyetFilter(generics.ListAPIView):
    serializer_class = MemnuniyetSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        mac_no = self.kwargs['mac_no']
        print(" get query set içinden -  memnuniyet -  mac no...", mac_no)
        memnuniyet = Memnuniyet.objects.filter(mac_no=mac_no)
        print("filtrelenen obje...", memnuniyet)
        return memnuniyet



class MemnuniyetQuery(generics.ListAPIView):
    serializer_class = MemnuniyetSerializer

    def get_queryset(self):
        """
        This view should return a list of all the mac list (actually must be one)
        for mac_no....
        """
        queryset = Memnuniyet.objects.all()
        mac_no = self.request.query_params.get('mac_no', None)
        if mac_no is not None:
            queryset = queryset.filter(mac_no=mac_no)
        return queryset


class MemnuniyetDetail(APIView):
    """
    Retrieve, update or delete a Memnuniyet instance.
    """
    def get_object(self, pk):
        try:
            return Memnuniyet.objects.get(pk=pk)
        except Memnuniyet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        memnuniyet = self.get_object(pk)
        serializer = MemnuniyetSerializer(memnuniyet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        memnuniyet = self.get_object(pk)
        print("def - put içinden memnuniyet objesi...", memnuniyet)
        serializer = MemnuniyetSerializer(memnuniyet, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        memnuniyet = self.get_object(pk)
        memnuniyet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#--------------------------------------------------------------------------------------------
# Operasyon data

class OperasyonRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = OperasyonSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return Operasyon_Data.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class OperasyonDetailView(APIView):
    def get(self, request, pk):
        operasyon_data = get_object_or_404(Operasyon_Data, pk=pk)
        serializer = OperasyonSerializer(operasyon_data)
        return Response(serializer.data)

    def delete(self, request, pk):
        operasyon_data = get_object_or_404(Operasyon_Data, pk=pk)
        operasyon_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class OperasyonList(APIView):
    """
    List all Operasyon Data (get), or create a new Operasyon Data (post).
    """
    def get(self, request, format=None):
        operasyon_data = Operasyon_Data.objects.all()
        serializer = OperasyonSerializer(operasyon_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OperasyonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OperasyonBul(APIView):
    """
    find id from mac_no.
    """
    def get(self, request, format=None):
        deger = 52812233799999999
        print("find object çalıştı..operasyon bul  api içinden ....", deger)
        operasyon_data = Operasyon_Data.objects.filter(mac_no=deger).first()
        print("operasyon mac.. filter sonucu...", operasyon_data)
        serializer = OperasyonSerializer(operasyon_data, many=True)
        return Response(serializer.data)

class OperasyonFilter(generics.ListAPIView):
    serializer_class = OperasyonSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        mac_no = self.kwargs['mac_no']
        print(" get query set içinden -  operasyon -  mac no...", mac_no)
        operasyon_data = Operasyon_Data.objects.filter(mac_no=mac_no)
        print("filtrelenen obje...", operasyon_data)
        return operasyon_data



class OperasyonQuery(generics.ListAPIView):
    serializer_class = OperasyonSerializer

    def get_queryset(self):
        """
        This view should return a list of all the mac list (actually must be one)
        for mac_no....
        """
        queryset = Operasyon_Data.objects.all()
        mac_no = self.request.query_params.get('mac_no', None)
        if mac_no is not None:
            queryset = queryset.filter(mac_no=mac_no)
        return queryset


class OperasyonDetail(APIView):
    """
    Retrieve, update or delete a Memnuniyet instance.
    """
    def get_object(self, pk):
        try:
            return Operasyon_Data.objects.get(pk=pk)
        except Operasyon_Data.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        operasyon_data = self.get_object(pk)
        serializer = OperasyonSerializer(operasyon_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        operasyon_data = self.get_object(pk)
        print("def - put içinden operasyon objesi...", operasyon_data)
        serializer = OperasyonSerializer(operasyon_data, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        operasyon_data = self.get_object(pk)
        operasyon_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#-----------------------------------------------------------------------------------------
# Denetim data


class DenetimRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = DenetimSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return Denetim_Data.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class DenetimDetailView(APIView):
    def get(self, request, pk):
        denetim_data = get_object_or_404(Denetim_Data, pk=pk)
        serializer = DenetimSerializer(denetim_data)
        return Response(serializer.data)

    def delete(self, request, pk):
        denetim_data = get_object_or_404(Denetim_Data, pk=pk)
        denetim_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class DenetimList(APIView):
    """
    List all Denetim  (get), or create a new Denetim (post).
    """
    def get(self, request, format=None):
        denetim_data = Denetim_Data.objects.all()
        serializer = DenetimSerializer(denetim_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DenetimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DenetimBul(APIView):
    """
    find id from mac_no.
    """
    def get(self, request, format=None):
        deger = 52812233799999999
        print("find object çalıştı..denetim bul  api içinden ....", deger)
        denetim_data = Denetim_Data.objects.filter(mac_no=deger).first()
        print("denetim mac.. filter sonucu...", denetim_data)
        serializer = DenetimSerializer(denetim_data, many=True)
        return Response(serializer.data)

class DenetimFilter(generics.ListAPIView):
    serializer_class = DenetimSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        mac_no = self.kwargs['mac_no']
        print(" get query set içinden -  denetim -  mac no...", mac_no)
        denetim_data = Denetim_Data.objects.filter(mac_no=mac_no)
        print("filtrelenen obje...", denetim_data)
        return denetim_data



class DenetimQuery(generics.ListAPIView):
    serializer_class = DenetimSerializer

    def get_queryset(self):
        """
        This view should return a list of all the mac list (actually must be one)
        for mac_no....
        """
        queryset = Denetim_Data.objects.all()
        mac_no = self.request.query_params.get('mac_no', None)
        if mac_no is not None:
            queryset = queryset.filter(mac_no=mac_no)
        return queryset


class DenetimDetail(APIView):
    """
    Retrieve, update or delete a Denetim instance.
    """
    def get_object(self, pk):
        try:
            return Denetim_Data.objects.get(pk=pk)
        except Denetim_Data.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        denetim_data = self.get_object(pk)
        serializer = DenetimSerializer(denetim_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        denetim_data = self.get_object(pk)
        print("def - put içinden denetim objesi...", denetim_data)
        serializer = DenetimSerializer(denetim_data, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        denetim_data = self.get_object(pk)
        denetim_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#-----------------------------------------------------------------------------------
# Ariza data


class ArizaRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = ArizaSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return Ariza_Data.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class ArizaDetailView(APIView):
    def get(self, request, pk):
        ariza_data = get_object_or_404(Ariza_Data, pk=pk)
        serializer = ArizaSerializer(ariza_data)
        return Response(serializer.data)

    def delete(self, request, pk):
        ariza_data = get_object_or_404(Ariza_Data, pk=pk)
        ariza_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ArizaList(APIView):
    """
    List all Ariza  (get), or create a new Ariza (post).
    """
    def get(self, request, format=None):
        ariza_data = Ariza_Data.objects.all()
        serializer = ArizaSerializer(ariza_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArizaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArizaBul(APIView):
    """
    find id from mac_no.
    """
    def get(self, request, format=None):
        deger = 52812233799999999
        print("find object çalıştı..ariza bul  api içinden ....", deger)
        ariza_data = Ariza_Data.objects.filter(mac_no=deger).first()
        print("ariza mac.. filter sonucu...", ariza_data)
        serializer = ArizaSerializer(ariza_data, many=True)
        return Response(serializer.data)


class ArizaFilter(generics.ListAPIView):
    serializer_class = ArizaSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        mac_no = self.kwargs['mac_no']
        print(" get query set içinden -  ariza -  mac no...", mac_no)
        ariza_data = Ariza_Data.objects.filter(mac_no=mac_no)
        print("filtrelenen obje...", ariza_data)
        return ariza_data



class ArizaQuery(generics.ListAPIView):
    serializer_class = ArizaSerializer

    def get_queryset(self):
        """
        This view should return a list of all the mac list (actually must be one)
        for mac_no....
        """
        queryset = Ariza_Data.objects.all()
        mac_no = self.request.query_params.get('mac_no', None)
        if mac_no is not None:
            queryset = queryset.filter(mac_no=mac_no)
        return queryset


class ArizaDetail(APIView):
    """
    Retrieve, update or delete a Ariza instance.
    """
    def get_object(self, pk):
        try:
            return Ariza_Data.objects.get(pk=pk)
        except Ariza_Data.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        ariza_data = self.get_object(pk)
        serializer = ArizaSerializer(ariza_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        ariza_data = self.get_object(pk)
        print("def - put içinden memnuniyet objesi...", ariza_data)
        serializer = ArizaSerializer(ariza_data, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        ariza_data = self.get_object(pk)
        ariza_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#--------------------------------------------------------------------------------------
# RFID data


class RfidRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = RfidSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return rfid_dosyasi.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class RfidDetailView(APIView):
    def get(self, request, pk):
        rfid_data = get_object_or_404(rfid_dosyasi, pk=pk)
        serializer = RfidSerializer(rfid_data)
        return Response(serializer.data)

    def delete(self, request, pk):
        rfid_data = get_object_or_404(rfid_dosyasi, pk=pk)
        rfid_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class RfidList(APIView):
    """
    List all Rfid  (get), or create a new Rfid (post).
    """
    def get(self, request, proje_no=None, format=None):
        pr_no = proje_no
        print(" rfidlist get içinden proje_no", pr_no)
        rfid_data = rfid_dosyasi.objects.all()
        serializer = RfidSerializer(rfid_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RfidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RfidBul(APIView):
    """
    find id from mac_no.
    """
    def get(self, request, format=None):
        deger = 52812233799999999
        print("find object çalıştı..rfid bul  api içinden ....", deger)
        rfid_data = rfid_dosyasi.objects.filter(mac_no=deger).first()
        print("rfid mac.. filter sonucu...", rfid_data)
        serializer = RfidSerializer(rfid_data, many=True)
        return Response(serializer.data)


class RfidFilter(generics.ListAPIView):
    serializer_class = RfidSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        proje = self.kwargs['proje']
        print(" get query set içinden -  rfid -  project...", proje)
        rfid_data = rfid_dosyasi.objects.filter(proje=proje)
        print("filtrelenen obje...", rfid_data)
        return rfid_data



class RfidQuery(generics.ListAPIView):
    serializer_class = RfidSerializer

    def get_queryset(self):
        """
        This view should return a list of all the mac list (actually must be one)
        for mac_no....
        """
        queryset = rfid_dosyasi.objects.all()
        mac_no = self.request.query_params.get('mac_no', None)
        if mac_no is not None:
            queryset = queryset.filter(mac_no=mac_no)
        return queryset


class RfidDetail(APIView):
    """
    Retrieve, update or delete a rfid instance.
    """
    def get_object(self, pk):
        try:
            return rfid_dosyasi.objects.get(pk=pk)
        except rfid_dosyasi.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        rfid_data = self.get_object(pk)
        serializer = RfidSerializer(rfid_data)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        rfid_data = self.get_object(pk)
        print("def - put içinden rfid objesi...", rfid_data)
        serializer = ArizaSerializer(rfid_data, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        rfid_data = self.get_object(pk)
        rfid_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#---------------------------------------------------------------------------------
# yer up down ws işlemleri

class YerudRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class        = YerudSerializer
    permission_classes      = [IsOwnerOrReadOnly]
    #queryset                = BlogPost.objects.all()
    @csrf_exempt
    def get_queryset(self):
        return yer_updown.objects.all()
    @csrf_exempt
    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class YerudDetailView(APIView):
    def get(self, request, pk):
        yerud_data = get_object_or_404(yer_updown, pk=pk)
        serializer = RfidSerializer(yerud_data)
        return Response(serializer.data)

    def delete(self, request, pk):
        yerud_data = get_object_or_404(yer_updown, pk=pk)
        yerud_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class YerudList(APIView):
    """
    List all yer up down (get), or create a new yer up down (post).
    """
    def get(self, request, format=None):
        yerud_data = yer_updown.objects.all()
        serializer = YerudSerializer(yerud_data, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = YerudSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YerudBul(APIView):
    """
    find id from mac_no.
    """
    def get(self, request, format=None):
        deger = 20
        print("find object çalıştı..yerud bul  api içinden ....", deger)
        """
        try:
            yerud_object = yer_updown.objects.get(pk=1)
        except MyModel.DoesNotExist:
            raise Http404("No MyModel matches the given query.")
        """
        #yerud_data = yer_updown.objects.filter(mac_no=deger).first()
        yerud_data = yer_updown.objects.get(mac_no=deger)
        print(" yerud mac.. filter sonucu...", yerud_data)
        serializer = YerudSerializer(yerud_data)
        return Response(serializer.data)


class YerudFilter(generics.ListAPIView):
    serializer_class = YerudSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        mac_no = self.kwargs['mac_no']
        print(" get query set içinden -  yerud -  mac no...", mac_no)
        yerud_data = yer_updown.objects.filter(mac_no=mac_no)
        print("filtrelenen obje...", yerud_data)
        return yerud_data



class YerudQuery(generics.ListAPIView):
    serializer_class = YerudSerializer

    def get_queryset(self):
        """
        This view should return a list of all the yerud list (actually must be one)
        for mac_no....
        """
        queryset = yer_updown.objects.all()
        mac_no = self.request.query_params.get('mac_no', None)
        if mac_no is not None:
            queryset = queryset.filter(mac_no=mac_no)
        return queryset


class YerudDetail(APIView):
    """
    Retrieve, update or delete a yerud instance.
    """
    def get_object(self, pk):
        try:
            return yer_updown.objects.get(mac_no=pk)
        except yer_updown.DoesNotExist:
            raise Http404

    def get_object_macno(self, macno):
        try:
            return yer_updown.objects.get(mac_no=macno)
        except yer_updown.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        yerud_data = self.get_object(pk)
        serializer = YerudSerializer(yerud_data)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        yerud_data = self.get_object(pk)
        print("def - put içinden yerud objesi...", yerud_data)
        serializer = YerudSerializer(yerud_data, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def macno_degis(self, request, macno, format=None):

        yerud_data = self.get_object_macno(macno)
        print("def - put içinden yerud objesi...", yerud_data)
        serializer = YerudSerializer(yerud_data, data=request.data)
        if serializer.is_valid():
            print(" serializer...", serializer)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        yerud_data = self.get_object(pk)
        yerud_data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
