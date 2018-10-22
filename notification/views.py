from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from .models import Notification
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import datetime

def show_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    return render_to_response('islem/bildirimler.html', {'notification': n})

def delete_notification(request, notification_id):
    n = Notification.objects.get(id=notification_id)
    n.viewed = True
    n.save()
    return redirect('list_notification')

def create_notification(request):
    print("create notification kısmı...")
    print("request.user.id", request.user.id)
    Notification.objects.create(kisi_id=request.user.id,
                                proje_id=2,
                                title="bildirim başlık ....",
                                message="bildirim mesaj.........2 numaralı proje için ")
    return redirect('index')


def list_notification(request):
    print("list notifications ..")
    print("request user id..", request.user.id)
    #n = Notification.objects.all()
    bugun = datetime.datetime.now()
    yedigun = datetime.timedelta(7,0,0)
    yedigun_once = bugun - yedigun
    print(bugun)
    print(yedigun_once)
    n_list = Notification.objects.filter(kisi_id=request.user.id).filter(timestamp__gt=yedigun_once).order_by("-id")
    #contact_list = Contacts.objects.all()
    paginator = Paginator(n_list, 20)
    page = request.GET.get('page')
    try:
        n = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        n = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        n = paginator.page(paginator.num_pages)
    print("işte sayfalanmış liste...", n)
    return render_to_response('islem/bildirimler_genel.html', {'notification_list': n})
