from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.urls import reverse

from .models import *


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect(reverse('Home'))


# Create your views here.
def schedule(request,year):
    name1 = f'Durga Puja Schedule for {year}'
    try: year,show=Year.objects.filter(year=year).get(), True
    except Year.DoesNotExist: show = False
    except: show=False

    if show:
        params = {
            'year':year,
            'show':show,
            'title':name1,
            'view':'schedule'
        }
    else:
        params = {
            'show':show,
            'title':name1,
            'view':'schedule',
            'yearpass': year
        }
    
    return render(
        request,
        'schedule.html',
        params
    )


def home(request):
    name1 = "Videos List"
    year = Year.objects.all()
    videos = Videos.objects.values('yearmodel').distinct().all()
    videoslive = Videos.objects.values('yearmodel','live').filter(live=True).all()
    return render(
        request,
        'playlist.html',
        {
            'year':year,
            'videos':videos, 
            'title':name1,
            'view': 'Home',
            'videoslive':videoslive
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
    try:
        yearid = Year.objects.values('id').filter(year=int(year)).get()['id']
        videos = Videos.objects.filter(yearmodel=yearid, day=day).all()
    except:
        from django.http import Http404
        raise Http404("The year in our database does not exist!")

    try:
        livevideo = Videos.objects.filter(yearmodel=yearid, live=True).values('day','live').get()
    except Videos.DoesNotExist:
        livevideo = Videos.objects.none()
    return render(
        request,'videos.html',
        {
            'videos':videos, 
            'title':name1,
            'yearpassed':year,
            'dayname':dayname.upper(),
            'lengthday': len(dayname),
            'view': '',
            'livevideo':livevideo
        }
    )



def handler404(request, *args, **argv):
    from datetime import datetime
    x = datetime.now()
    return render(
        None,
        '404.html', 
        {
            'title':'404 Ohh Snap!!! Sorry!',
            'yearpassed': x.strftime("%Y")
        }
    )


def handler500(request, *args, **argv):
    from datetime import datetime
    x = datetime.now()
    return  render(
        None,
        '500.html', 
        {
            'title':'500 Ohh Snap!!! Sorry!',
            'yearpassed': x.strftime("%Y")
        }
    )
