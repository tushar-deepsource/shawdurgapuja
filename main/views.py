from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect(reverse('Home'))


# Create your views here.
def pdf(request,file_path):
    return HttpResponse(f'<embed type="application/pdf" src="{file_path}" width="100%" height="100%">')


def home(request):
    name1 = "Videos List"
    year = Year.objects.all()
    videos = Videos.objects.values('yearmodel').distinct().all()
    return render(
        request,
        'playlist.html',
        {
            'year':year,
            'videos':videos, 
            'title':name1,
            'view': 'Home'
        }
    ) 


def video(request,year,day):
    day = day.upper()
    if day == 'S': dayname = "Shashti"
    elif day == 'SA': dayname = "Sapatami"
    elif day == 'A': dayname = "Ashtami"
    elif day == 'SAN': dayname = "Sandhi"
    elif day == 'N': dayname = "Navami"
    elif day == 'D': dayname = "Dashami"
    else: raise Http404("The day you requested in not available")
    
    name1 = f"Maha {dayname}"
    yearid = Year.objects.values('id').filter(year=int(year)).get()['id']

    videos = Videos.objects.filter(yearmodel=yearid, day=day).all()
    return render(
        request,'videos.html',
        {
            'videos':videos, 
            'title':name1,
            'yearpassed':year,
            'dayname':dayname.upper(),
            'lengthday': len(dayname),
            'view': ''
        }
    )
