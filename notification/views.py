from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from .models import Notification
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


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
    Notification.objects.create(user_id=request.user.id,
                                title="8 nisan uyarı  1",
                                message="8 nisan uyarı...111")
    return redirect('index')


def list_notification(request):
    print("list notifications ..")
    print("request user id..", request.user.id)
    #n = Notification.objects.all()
    n_list = Notification.objects.filter(viewed=False).order_by("-id")
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
    return render_to_response('islem/bildirimler.html', {'notification_list': n})
