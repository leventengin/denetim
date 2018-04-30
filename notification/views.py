from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from .models import Notification
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404


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
    n = Notification.objects.filter(viewed=False)
    return render_to_response('islem/bildirimler.html', {'notification_list': n})
