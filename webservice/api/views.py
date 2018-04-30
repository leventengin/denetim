# generic
from django.db import models
from django.db.models import Q
from rest_framework import generics, mixins
from django.views.decorators.csrf import csrf_exempt
from ..models import BlogPost, MacPost, Memnuniyet
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer, MacPostSerializer, MemnuniyetSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view



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


    # def get_object(self):
    #     pk = self.kwargs.get("pk")
#     return BlogPost.objects.get(pk=pk)




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
        memnunyet = get_object_or_404(Memnuniyet, pk=pk)
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
