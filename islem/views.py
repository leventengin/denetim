from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
from .models import Profile, denetim, gozlemci, sonuc, sonuc_bolum
from django.shortcuts import render, redirect, get_object_or_404
from django.db import models, transaction
from islem.forms import GozlemciForm, BolumSecForm, DetayForm
import collections


#-------------------------------------------------------------------------------
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from weasyprint import HTML, CSS
from django.template.loader import render_to_string








class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'today': datetime.date.today(),
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
            }
        #pdf = render_to_pdf('pdf/invoice.html', data)
        pdf = render_to_pdf('pdf/utf8.html')
        return HttpResponse(pdf, content_type='application/pdf')


class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        denetim_no = request.session.get('denetim_no')
        denetim_obj = denetim.objects.get(id=denetim_no)
        print("seçilen denetim", denetim_obj)
        denetim_adi = denetim_obj.denetim_adi
        musteri = denetim_obj.musteri
        denetci = denetim_obj.denetci
        tipi = denetim_obj.tipi
        yaratim_tarihi = denetim_obj.yaratim_tarihi
        yaratan = denetim_obj.yaratan
        hedef_baslangic = denetim_obj.hedef_baslangic
        hedef_bitis = denetim_obj.hedef_bitis
        gerc_baslangic = denetim_obj.gerc_baslangic
        gerc_bitis = denetim_obj.gerc_bitis
        d = collections.defaultdict(list)
        bolum_obj = sonuc_bolum.objects.filter(denetim=denetim_no)
        for bolum in bolum_obj:
            print("bolum list . bolum", bolum.bolum)
            detay_obj = sonuc.objects.filter(denetim=denetim_no, bolum=bolum.bolum)
            for detay in detay_obj:
                print("detay list . detay", detay.bolum, detay.detay)
                d[detay.bolum].append(detay.detay)
        print("***********************")
        print(d)
        d.default_factory = None
        dict_bol_detay = dict(d)
        print("************************")
        print(dict_bol_detay)
        context = {'dict_bol_detay':dict_bol_detay,
                    'denetim_adi': denetim_adi,
                    'musteri' : musteri,
                    'denetci' : denetci,
                    'tipi' : tipi,
                    'yaratim_tarihi' : yaratim_tarihi,
                    'yaratan' : yaratan,
                    'hedef_baslangic' : hedef_baslangic,
                    'hedef_bitis' : hedef_bitis,
                    }
        template = get_template('pdf/is_emri.html')
        html = template.render(context).encode("UTF-8")
        page = HTML(string=html, encoding='utf-8').write_pdf()
        response = HttpResponse(page, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report_example.pdf"'
        return response




"""
        pdf = render_to_pdf('pdf/is_emri.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Denetim_Dosyası_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

"""

#-------------------------------------------------------------------------------



@login_required
def report_example(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #varModel = Model.objects.all()
    template = get_template('pdf/weasyprint.html')
    context = {}
    context = {'denetim_obj': denetim_obj, }
    html = template.render(context).encode("UTF-8")
    page = HTML(string=html, encoding='utf-8').write_pdf()
    response = HttpResponse(page, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report_example.pdf"'
    return response




#------------------------------------------------------------------------------

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
# detayların puanlanması ve foto yüklenmesi .....


from .forms import DetayForm


def upload_file(request):
    if request.method == 'POST':
        form = SonucForm(request.POST, request.FILES)
        if form.is_valid():
            instance = sonuc(foto=request.FILES['file'])
            instance.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = SonucForm()
    return render(request, 'upload.html', {'form': form})



#--------------------------------------------------------------------------------

@login_required
def index(request):
    kisi = request.user
    print("kisi", kisi)
    kullanici = Profile.objects.get(user=kisi)
    print("kullanıcı", kullanici)

    if kullanici.denetci == "E":
        acik_denetimler = denetim.objects.filter(durum="B") | denetim.objects.filter(durum="Y")
        acik_denetimler_sirali = acik_denetimler.order_by('hedef_baslangic')
        secili_denetimler = acik_denetimler_sirali.filter(denetci=request.user)
        return render(request, 'ana_menu.html',
            context={
            'secili_denetimler': secili_denetimler,
            },
        )
    else:
        return render(request, 'ana_menu_2.html',)


"""
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
"""


#------------------------------------------------------------------------------


@login_required
def denetim_detay(request, pk=None):

    request.session['denetim_no'] = pk
    request.session.modified = True

    denetim_obj = denetim.objects.get(id=pk)
    print("seçilen denetim", denetim_obj)
    denetim_adi = denetim_obj.denetim_adi
    musteri = denetim_obj.musteri
    denetci = denetim_obj.denetci
    tipi = denetim_obj.tipi
    yaratim_tarihi = denetim_obj.yaratim_tarihi
    yaratan = denetim_obj.yaratan
    hedef_baslangic = denetim_obj.hedef_baslangic
    hedef_bitis = denetim_obj.hedef_bitis
    gerc_baslangic = denetim_obj.gerc_baslangic
    gerc_bitis = denetim_obj.gerc_bitis
    durum = denetim_obj.durum
    d = collections.defaultdict(list)
    bolum_obj = sonuc_bolum.objects.filter(denetim=pk)
    for bolum in bolum_obj:
        print("bolum list . bolum", bolum.bolum)
        detay_obj = sonuc.objects.filter(denetim=pk, bolum=bolum.bolum)
        for detay in detay_obj:
            print("detay list . detay", detay.bolum, detay.detay)
            d[detay.bolum].append(detay.detay)
    print("***********************")
    print(d)
    d.default_factory = None
    dict_bol_detay = dict(d)
    print("************************")
    print(dict_bol_detay)
    context = {'dict_bol_detay':dict_bol_detay,
               'denetim_adi': denetim_adi,
               'musteri' : musteri,
               'denetci' : denetci,
               'tipi' : tipi,
               'yaratim_tarihi' : yaratim_tarihi,
               'yaratan' : yaratan,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               'durum' : durum,
               }
    return render(request, 'ana_menu_2.html', context )



#--------------------------------------------------------------------------------

@login_required
def denetim_baslat(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim", denetim_obj)

    denetim_adi = denetim_obj.denetim_adi
    musteri = denetim_obj.musteri
    yaratim_tarihi = denetim_obj.yaratim_tarihi

    hedef_baslangic = denetim_obj.hedef_baslangic
    hedef_bitis = denetim_obj.hedef_bitis

    context = {'denetim_adi': denetim_adi,
               'musteri' : musteri,
               'yaratim_tarihi' : yaratim_tarihi,
               'hedef_baslangic' : hedef_baslangic,
               'hedef_bitis' : hedef_bitis,
               }
    return render(request, 'islem/denetim_baslat_sor.html', context )



#--------------------------------------------------------------------------------

@login_required
def denetim_baslat_kesin(request, pk=None):

    denetim_no = request.session.get('denetim_no')
    denetim_obj = denetim.objects.get(id=denetim_no)
    print("seçilen denetim kesin ...", denetim_obj)
    denetim_obj.durum = "Y"
    denetim_obj.save()
    return redirect('denetim_bolum_sec' )



#--------------------------------------------------------------------------------


@login_required
def denetim_bolum_sec(request, pk=None):

    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('denetim_no')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = BolumSecForm(request.POST or None)
        print("buraya mı geldi...  denetim_bolum_sec...POST")
        if form.is_valid():
            bolum = request.POST.get('bolum', "")
            print ("bolum", bolum)
            request.session["secili_bolum"] = bolum
            detaylar = sonuc.objects.filter(denetim=denetim_no).filter(bolum=bolum)
            for detay in detaylar:
                detay.tamam = "H"
            form = DetayForm(denetim_no=denetim_no, secili_bolum=secili_bolum)
            return render(request, 'islem/denetim_detay_islemleri.html')


        else:
            return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        form = BolumSecForm(denetim_no=denetim_no)
        return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})



#--------------------------------------------------------------------------

def secilen_bolumu_kaydet(request):
    print("seçilen bölümü kaydet ......")
    response_data ={}
    if request.method == 'GET':
        selected = request.GET.get('selected', None)
        print("selected...:", selected )
        selected_obj = sonuc_bolum.objects.get(id=selected)
        print("selected obj", selected_obj)
        selected_bol = selected_obj.bolum.id
        print("selected_bol", selected_bol)
        if selected_bol != None:
            request.session['secili_bolum'] = selected_bol
            request.session.modified = True
            print("secili bölüm burada...:", request.session['secili_bolum'])
        else:
            print("selected none  .....  neler oluyor !!!!!")
    return HttpResponse(response_data, content_type='application/json')





#--------------------------------------------------------------------------------




@login_required
def detay_islemleri_baslat(request, pk=None):
    print("denetim işlemleri başlat......")
    response_data ={}
    if request.method == 'GET':
        denetim_no = request.session.get('denetim_no')
        secili_bolum = request.session.get('secili_bolum')
        # selected = request.GET.get('selected', None)
        print("denetim no...:", denetim_no )
        print("secili bolum...", secili_bolum)
        ilk_detaylar = sonuc.objects.filter(denetim=denetim_no)
        print("ilk detaylar..:", ilk_detaylar)
        detaylar = ilk_detaylar.filter(bolum=secili_bolum)
        print("detaylar..:", detaylar)
        if not detaylar:
            messages.success(request, 'Seçili bölümde bölüm detayı yok....')
            return redirect('denetim_baslat')
        for detay in detaylar:
            print("bolum id for loop içinden", detay.bolum.id, "ve detay id", detay.detay.id)
            detay.tamam = "H"
            detay.save()
        return HttpResponse(response_data, content_type='application/json')


"""
        secili_detay_obj = detaylar.first()
        secili_detay = secili_detay_obj.detay.id
        print("ilk - secili - detay.... bakalım  doğru mu...", secili_detay)
        request.session['secili_detay'] = secili_detay
        form = DetayForm()
        context = { 'form': form,
                    'denetim_no' : denetim_no,
                    'secili_bolum' : secili_bolum,
                    'secili_detay' : secili_detay,
                    }
        return render(request, 'islem/denetim_detay_islemleri.html', context)
"""

#--------------------------------------------------------------------------------


@login_required
def denetim_detay_islemleri(request, pk=None):

    # if this is a POST request we need to process the form data
    denetim_no = request.session.get('denetim_no')
    secili_bolum = request.session.get('secili_bolum')
    secili_detay = request.session.get('secili_detay')
    print("denetim detay işlemleri...................")
    print("denetim_no", denetim_no)
    print("secili_bolum", secili_bolum)
    print("secili_detay", secili_detay)


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DetayForm(request.POST or None)
        print("buraya mı geldi...  denetim_detay işlemleri...POST")
        if form.is_valid():
            bolum = request.POST.get('bolum', "")
            print ("bolum", bolum)
            request.session["secili_bolum"] = bolum
            detaylar = sonuc.objects.filter(denetim=denetim_no).filter(bolum=bolum)
            for detay in detaylar:
                detay.tamam = "H"
            form = DetayForm(denetim_no=denetim_no, secili_bolum=secili_bolum)
            return render(request, 'islem/denetim_detay_islemleri.html')

        else:
            return render(request, 'islem/denetim_bolum_sec.html', {'form': form,})

    # if a GET (or any other method) we'll create a blank form
    else:
        ilk_detaylar = sonuc.objects.filter(denetim=denetim_no)
        print("ilk detaylar..denetim detay işlemleri :", ilk_detaylar)
        detaylar = ilk_detaylar.filter(bolum=secili_bolum)
        print("detaylar.. denetim detay işişlemleri..:", detaylar)
        secili_detay_obj = detaylar.filter(tamam="H")
        print("seçili detaylar tamam H olanlar...", secili_detay_obj)

        if not secili_detay_obj:
            messages.success(request, 'Bölüm içinde detay işlemleri tamamlandı....')
            return redirect('denetim_bolum_sec')

        for detay in secili_detay_obj:
            secili_detay = detay.detay.id
            print("secili - detay.... bakalım  doğru mu...", secili_detay)
            request.session['secili_detay'] = secili_detay
            form = DetayForm()
            context = { 'form': form,
                        'detay' : detay,
                        }
            return render(request, 'islem/denetim_detay_islemleri.html', context)

        return redirect('denetim_bolum_sec')

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
# gözlemci seçimi ile ilgili bölümler.....
#-----------------------------------------------------

@login_required
def gozlemci_sec(request, pk=None):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GozlemciForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            kisi = request.POST.getlist('kisi', "")
            print ("kisi", kisi)
            #import pdb; pdb.set_trace()
            #kaydetme_obj = deneme_giris(yazi = isim, user = kullanici, tarih = tarih)
            #kaydetme_obj.save()
            #text = form.cleaned_data["your_name"]
            #myQS = yedek_parca.objects.none()
            form = GozlemciForm()
            messages.success(request, 'Başarıyla kaydetti....')
            return redirect('gozlemci_sec')
        else:
            return render(request, 'islem/denetim_takipcisi.html', {'form': form,})


    # if a GET (or any other method) we'll create a blank form
    else:
        #selected_alt = request.session.get('selected_alt')
        form = GozlemciForm()
        #deneme_giris_QS = deneme_giris.objects.all().order_by('-tarih')
        #args = {'form': form, 'deneme_giris_QS': deneme_giris_QS}
        #import pdb; pdb.set_trace()
        #return render(request, 'name.html', args)
        return render(request, 'islem/denetim_takipcisi.html', {'form': form,})


#---------------------------------------------------------------------

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

# -*- coding: utf-8 -*-
from .models import denetim
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.http import HttpResponse



# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.template import Context


def generate_pdf(request):
    """Generate pdf."""
    # Model data
    denetim_obj = denetim.objects.all().order_by('denetim_adi')

    # Rendered
    html_string = render_to_string('pdf/weasyprint.html', {'denetim_obj': denetim_obj}).encode('utf-8')
    html = HTML(string=html_string)

    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=list_people.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'r')
        response.write(output.read())

    return response





#-------------------------------------------------------------------------------

def xyz(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #content = unicode(content)
    #denetim_obj = str(denetim_obj)
    return render(request, 'islem/xyz.html', {'denetim_obj': denetim_obj} )


#-------------------------------------------------------------------------------

def kamera(request):
    denetim_obj = denetim.objects.all().order_by('denetim_adi')
    #content = unicode(content)
    #denetim_obj = str(denetim_obj)
    return render(request, 'islem/kamera.html', {'denetim_obj': denetim_obj} )
