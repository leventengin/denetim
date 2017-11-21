from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template.loader import get_template
from islem.utils import render_to_pdf #created in step 4
import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import grup, sirket, musteri, tipi, bolum, detay
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models, transaction






class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            }
        pdf = render_to_pdf('pdf/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        template = get_template('pdf/invoice.html')
        context = {
            "invoice_id": 123,
            "order_id": 1233434,
            "customer_name": "John Cooper",
            "amount": 1399.99,
            "today": "Today",
        }
        html = template.render(context)
        pdf = render_to_pdf('pdf/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


def eposta_gonder(request):
    subject = 'konusu bu'
    from_email = settings.EMAIL_HOST_USER
    to_email = ['lvengin@yahoo.com', 'lvengin@gmail.com']
    email_message = ' ilk deneme bu .....'
    send_mail(subject,
              email_message,
              from_email,
              to_email,
              fail_silently=False)

#---------------------------------------------------------------------------------


@login_required
def index(request):
    num_tipi=tipi.objects.all().count()
    num_bolum=bolum.objects.all().count()
    num_detay=detay.objects.all().count()

    num_grup=grup.objects.all().count()
    num_sirket=sirket.objects.all().count()
    num_musteri=musteri.objects.count()

    return render(request, 'ana_menu.html',
        context={
        'num_tipi':num_tipi,
        'num_bolum':num_bolum,
        'num_detay':num_detay,

        'num_grup': num_grup,
        'num_sirket': num_sirket,
        'num_musteri': num_musteri,
        },
    )



#--------------------------------------------------------------------------------


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#------------------------------------------------------

@login_required
def tipi_sil(request, pk=None):
    print("tip sildeki pk:", pk)
    object = get_object_or_404(tip, pk=pk)
    sil_tip = object.tip_adi
    sil_id = object.id
    print("sil_tip", sil_tip)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_tip': sil_tip, 'pk': pk,}
    return render(request, 'islem/tipi_sil_soru.html', args)


@login_required
def tipi_sil_kesin(request, pk=None):
    print("tip sil kesindeki pk:", pk)
    object = get_object_or_404(tip, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('tipi')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('tipi')


#------------------------------------------------------

@login_required
def bolum_sil(request, pk=None):
    print("bolum sildeki pk:", pk)
    object = get_object_or_404(bolum, pk=pk)
    sil_bolum = object.bolum_adi
    sil_id = object.id
    print("sil_bolum", sil_bolum)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_bolum': sil_bolum, 'pk': pk,}
    return render(request, 'islem/bolum_sil_soru.html', args)


@login_required
def bolum_sil_kesin(request, pk=None):
    print("bolum sil kesindeki pk:", pk)
    object = get_object_or_404(bolum, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('bolum')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('bolum')

#------------------------------------------------------

@login_required
def detay_sil(request, pk=None):
    print("detay sildeki pk:", pk)
    object = get_object_or_404(detay, pk=pk)
    sil_detay = object.detay_adi
    sil_id = object.id
    print("sil_detay", sil_detay)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_detay': sil_detay, 'pk': pk,}
    return render(request, 'islem/detay_sil_soru.html', args)


@login_required
def detay_sil_kesin(request, pk=None):
    print("detay sil kesindeki pk:", pk)
    object = get_object_or_404(detay, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('detay')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('detay')




#------------------------------------------------------

@login_required
def grup_sil(request, pk=None):
    print("grup sildeki pk:", pk)
    object = get_object_or_404(grup, pk=pk)
    sil_grup = object.grup_adi
    sil_id = object.id
    print("sil_grup", sil_grup)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_grup': sil_grup, 'pk': pk,}
    return render(request, 'islem/grup_sil_soru.html', args)


@login_required
def grup_sil_kesin(request, pk=None):
    print("grup sil kesindeki pk:", pk)
    object = get_object_or_404(grup, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('grup')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('grup')


#------------------------------------------------------

@login_required
def sirket_sil(request, pk=None):
    print("sirket sildeki pk:", pk)
    object = get_object_or_404(sirket, pk=pk)
    sil_sirket = object.sirket_adi
    sil_id = object.id
    print("sil_sirket", sil_sirket)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_sirket': sil_sirket, 'pk': pk,}
    return render(request, 'islem/sirket_sil_soru.html', args)


@login_required
def sirket_sil_kesin(request, pk=None):
    print("sirket sil kesindeki pk:", pk)
    object = get_object_or_404(sirket, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('sirket')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('sirket')

#------------------------------------------------------

@login_required
def musteri_sil(request, pk=None):
    print("musteri sildeki pk:", pk)
    object = get_object_or_404(musteri, pk=pk)
    sil_musteri = object.musteri_adi
    sil_id = object.id
    print("sil_musteri", sil_musteri)
    print("sil_id", sil_id)
    args = {'sil_id': sil_id, 'sil_musteri': sil_musteri, 'pk': pk,}
    return render(request, 'islem/musteri_sil_soru.html', args)


@login_required
def musteri_sil_kesin(request, pk=None):
    print("musteri sil kesindeki pk:", pk)
    object = get_object_or_404(musteri, pk=pk)
    try:
        object.delete()
    except ProtectedError:
        error_message = "bağlantılı veri var,  silinemez...!!"
        #return JsonResponse(error_message, safe=False)
        messages.success(request, 'Bağlantılı veri var silinemez.......')
        return redirect('musteri')
    messages.success(request, 'Başarıyla silindi....')
    return redirect('musteri')




#------------------------------------------------------

# tipi yaratma, güncelleme, silme ...

class TipiCreate(LoginRequiredMixin,CreateView):
    model = tipi
    fields = '__all__'
    success_url = "/islem/tipi/create/"

class TipiUpdate(LoginRequiredMixin,UpdateView):
    model = tipi
    fields = '__all__'
    success_url = "/islem/tipi/"

class TipiDelete(LoginRequiredMixin,DeleteView):
    model = tipi
    success_url = reverse_lazy('tipi')



#-------------------------------------------------------------

# bolum yaratma, güncelleme, silme ...

class BolumCreate(LoginRequiredMixin,CreateView):
    model = bolum
    fields = '__all__'
    success_url = "/islem/bolum/create/"

class BolumUpdate(LoginRequiredMixin,UpdateView):
    model = bolum
    fields = '__all__'
    success_url = "/islem/bolum/"

class BolumDelete(LoginRequiredMixin,DeleteView):
    model = bolum
    success_url = reverse_lazy('bolum')



#------------------------------------------------------

# detay yaratma, güncelleme, silme ...

class DetayCreate(LoginRequiredMixin,CreateView):
    model = detay
    fields = '__all__'
    success_url = "/islem/detay/create/"

class DetayUpdate(LoginRequiredMixin,UpdateView):
    model = detay
    fields = '__all__'
    success_url = "/islem/detay/"

class DetayDelete(LoginRequiredMixin,DeleteView):
    model = detay
    success_url = reverse_lazy('detay')



#-------------------------------------------------------

# grup yaratma, güncelleme, silme ...

class GrupCreate(LoginRequiredMixin,CreateView):
    model = grup
    fields = '__all__'
    success_url = "/islem/grup/create/"

class GrupUpdate(LoginRequiredMixin,UpdateView):
    model = grup
    fields = '__all__'
    success_url = "/islem/grup/"

class GrupDelete(LoginRequiredMixin,DeleteView):
    model = grup
    success_url = reverse_lazy('grup')



#--------------------------------------------------------

# şirket yaratma, güncelleme, silme ...

class SirketCreate(LoginRequiredMixin,CreateView):
    model = sirket
    fields = '__all__'
    success_url = "/islem/sirket/create/"

class SirketUpdate(LoginRequiredMixin,UpdateView):
    model = sirket
    fields = '__all__'
    success_url = "/islem/sirket/"

class SirketDelete(LoginRequiredMixin,DeleteView):
    model = sirket
    success_url = reverse_lazy('sirket')



#-------------------------------------------------------

# musteri yaratma, güncelleme, silme ...

class MusteriCreate(LoginRequiredMixin,CreateView):
    model = musteri
    fields = '__all__'
    success_url = "/islem/musteri/create/"

class MusteriUpdate(LoginRequiredMixin,UpdateView):
    model = musteri
    fields = '__all__'
    success_url = "/islem/musteri/"

class MusteriDelete(LoginRequiredMixin,DeleteView):
    model = musteri
    success_url = reverse_lazy('musteri')




#------------------------------------------------------------

class TipiListView(LoginRequiredMixin,generic.ListView):
    model = tipi
    #paginate_by = 20

class TipiDetailView(LoginRequiredMixin,generic.DetailView):
    model = tipi

#--------------------------------------------------------------

class BolumListView(LoginRequiredMixin,generic.ListView):
    model = bolum
    #paginate_by = 20

class BolumDetailView(LoginRequiredMixin,generic.DetailView):
    model = bolum

#-----------------------------------------------------------

class DetayListView(LoginRequiredMixin,generic.ListView):
    model = detay

class DetayDetailView(LoginRequiredMixin,generic.DetailView):
    model = detay

#--------------------------------------------------------------

class GrupListView(LoginRequiredMixin,generic.ListView):
    model = grup
    #paginate_by = 20

class GrupDetailView(LoginRequiredMixin,generic.DetailView):
    model = grup

#---------------------------------------------------------

class SirketListView(LoginRequiredMixin,generic.ListView):
    model = sirket
    #paginate_by = 20

class SirketDetailView(LoginRequiredMixin,generic.DetailView):
    model = sirket

#------------------------------------------------------------

class MusteriListView(LoginRequiredMixin,generic.ListView):
    model = musteri

class MusteriDetailView(LoginRequiredMixin,generic.DetailView):
    model = musteri

#--------------------------------------------------------------
