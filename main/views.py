from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *
from datetime import datetime


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
    try:
        yearid = Year.objects.values('id').filter(year=int(year)).get()['id']
    except:
        raise Http404("The year in our database does not exist!")

    day = day.upper()
    if day in ('E','DI','T','C','P'): return redirect(reverse('Videos',args=[int(year),'MAA']))
    elif day == 'S': dayname = "Shashti"
    elif day == 'SA': dayname = "Sapatami"
    elif day == 'A': dayname = "Ashtami"
    elif day == 'SAN': dayname = "Sandhi"
    elif day == 'N': dayname = "Navami"
    elif day == 'D': dayname = "Dashami"
    elif day == 'MAA':
        try: maahome = Year.objects.filter(year=int(year)).values('maacomevid').get()['maacomevid']
        except IndexError: return redirect(reverse('Videos', args=[2020,'S']))
        if not maahome:
            raise Http404("The day you requested in not available")
    else: raise Http404("The day you requested in not available")
    
    if day == 'MAA': 
        videos = Videos.objects.filter(yearmodel=yearid, day__in=['E','DI','T','C','P']).iterator()
        try: day = videos[0].day
        except IndexError: return redirect(reverse('Videos',args=[2020,'S']))
        if day == 'E': dayname = "Ekami"
        elif day == 'DI': dayname = "Dvutia"
        elif day == 'T': dayname = "Tritiya"
        elif day == 'C': dayname = "Chathurti"
        elif day == 'P': dayname = "Panchami"
    else: videos = Videos.objects.filter(yearmodel=yearid, day=day).iterator()
    show = False if videos.count() <= 0 else True

    try: livevideo = Videos.objects.filter(yearmodel=yearid, live=True).values('day','live').get()
    except Videos.DoesNotExist: livevideo = Videos.objects.none()

    maahome = Year.objects.filter(year=int(year)).values('maacomevid').get()['maacomevid']

    return render(
        request,'videos.html',
        {
            'videos':videos, 
            'title':f"Maha {dayname}",
            'yearpassed':year,
            'dayname':dayname.upper(),
            'lengthday': len(dayname),
            'view': '',
            'livevideo':livevideo,
            'show': show,
            'maahome':maahome,
            'day':day
        }
    )

def about_year(request, year): 
    try:
        yearid = Year.objects.filter(year=int(year)).get()
    except:
        raise Http404("The year in our database does not exist!")
    return render(
        request,'about_year.html',
        {
            'yearpassed': year,
            'title': f'About the year puja {year}',
            'year': yearid ,
            'view': 'about',
        }
    )


def redirect_view_puja(request):
    #Year
    x = datetime.now()
    year = x.strftime("%Y")
    try: 
        yearid = Year.objects.values('id').filter(year=int(year)).get()['id']
    except Year.DoesNotExist: 
        yearid=None
        return redirect(reverse('Home'))

    #Day requiring
    try: 
        videodict = Videos.objects.filter(yearmodel=yearid,live=True).values('day').get()
    except: 
        videodict={'day':'None'}
        try:
            videodict = Videos.objects.filter(yearmodel=yearid).values('day').latest('yearmodel','day')
        except: 
            return redirect(reverse('Home'))

    #redirecting the user to the correct page
    return redirect(reverse('Videos',args=[int(year),videodict['day']])+'#live')



##Error 404
def handler404(request, *args, **argv):
    x = datetime.now()
    return render(
        None,
        '404.html', 
        {
            'title':'404 Ohh Snap!!! Sorry!',
            'yearpassed': x.strftime("%Y")
        }
    )

#Error 500
def handler500(request, *args, **argv):
    x = datetime.now()
    return  render(
        None,
        '500.html', 
        {
            'title':'500 Ohh Snap!!! Sorry!',
            'yearpassed': x.strftime("%Y")
        }
    )
