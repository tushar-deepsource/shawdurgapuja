import urllib.request
import datetime

import bangla
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.views.decorators.http import require_GET
from PIL import Image, ImageDraw, ImageFont, ImageOps

from .models import *


def arcproxy(request):
    with urllib.request.urlopen('https://arc.io/arc-sw.js') as response:
        return HttpResponse(response.read(),content_type='application/javascript')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect(reverse('Home'))

def changelang(request):
    old_lang = translation.to_locale(translation.get_language())
    l = request.META.get('HTTP_REFERER') if request.META.get('HTTP_REFERER') else reverse('Home')
    if old_lang == 'en':
        translation.activate("bn")
        return redirect(l.replace('en','bn'))
    else:
        translation.activate("en")
        return redirect(l.replace('bn','en')) 

#Images Api, which generates the cards images
@require_GET
def getimages(request):
    if os.path.isdir(os.path.join(settings.BASE_DIR, 'yearpic')): pass
    else: os.mkdir(os.path.join(settings.BASE_DIR, 'yearpic'))
    
    text = request.GET['text']
    back = request.GET.get('back','#FFF00C')
    textc = request.GET.get('textc','#496d89')
    
    img = Image.new('RGBA', (100, 30),color = str(back))
    d = ImageDraw.Draw(img)
    w, h = d.textsize(str(text))
    
    if request.LANGUAGE_CODE == 'bn' and text.replace('/','').isdigit():
        font = os.path.join(settings.BASE_DIR,'main','static','fonts','Baloo_Da-Regular.ttf')
        text = bangla.convert_english_digit_to_bangla_digit(str(text))
        d.text(((100-w)/2,(25-h)/2), str(text), fill=str(textc),font=ImageFont.truetype(font,11,layout_engine=ImageFont.LAYOUT_RAQM))
    else:
        d.text(((100-w)/2,(30-h)/2), str(text), fill=str(textc))
    
    output_image = os.path.join(settings.MEDIA_ROOT, "yearpic", str(text) + 'output' +'.png')
    main_image = os.path.join(settings.MEDIA_ROOT, "yearpic", str(text) + '.png')
    
    #Try Except Block
    output_image1 = output_image
    try: img.save(output_image1)
    except:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, "yearpic"))
        img.save(output_image1)

    #Making the image circular
    mask = Image.open(os.path.join(settings.BASE_DIR,'main','imagesreq','mask.png')).convert('L')
    im = Image.open(output_image)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    #Saving the cropped Image
    main_image1 = main_image
    output.save(main_image1)
    with open(main_image1, "rb") as image_file:
        image_data = image_file.read()
    #Deleting the first image made
    os.remove(output_image1)
    os.remove(main_image1)
    return HttpResponse(image_data, content_type="image/jpeg")
        


# Create your views here.
def homeredirect(request):
    return redirect(reverse('Home'))
    
@require_GET
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

@require_GET
def home(request):
    name1 = "Videos List"
    year = Year.objects.all()
    videos = Videos.objects.distinct('yearmodel')
    videoslive = Videos.objects.values('yearmodel','live').filter(live=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(year,6)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(
        request,
        'playlist.html',
        {
            'yearmodel':page_obj,
            'videos':videos, 
            'title':name1,
            'view': 'Home',
            'videoslive':videoslive
        }
    ) 

@require_GET
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
        except IndexError: return redirect(reverse('Videos', args=[int(year),'S']))
        if not maahome:
            raise Http404("The day you requested in not available")
    else: raise Http404("The day you requested in not available")
    
    if day == 'MAA': 
        videos = Videos.objects.filter(yearmodel=yearid, day__in=['E','DI','T','C','P']).all()
        try: day = videos[0].day
        except IndexError: return redirect(reverse('Videos',args=[int(year),'S']))
        if day == 'E': dayname = "Ekami"
        elif day == 'DI': dayname = "Dvutia"
        elif day == 'T': dayname = "Tritiya"
        elif day == 'C': dayname = "Chathurti"
        elif day == 'P': dayname = "Panchami"
    else: videos = Videos.objects.filter(yearmodel=yearid, day=day).all()
    show = False if videos.count() <= 0 else True

    livevideo = Videos.objects.filter(yearmodel=yearid, live=True).values('day','live').exists()
    if not livevideo: livevideo = Videos.objects.none()
    
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

@require_GET
def about_year(request, year): 
    try:
        yearid = Year.objects.filter(year=int(year)).get()
    except:
        raise Http404("The year in our database does not exist!")
    img_dir = os.listdir(settings.BASE_DIR / os.path.join('main','static','img'))
    addimg = lambda a: 'img/'+a
    return render(
        request,'about_year.html',
        {
            'yearpassed': year,
            'title': f'About the year puja {year}',
            'year': yearid ,
            'view': 'about',
            'img_dir': list(map(addimg,img_dir)),
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
    x = datetime.datetime.now()
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
    x = datetime.datetime.now()
    return  render(
        None,
        '500.html', 
        {
            'title':'500 Ohh Snap!!! Sorry!',
            'yearpassed': x.strftime("%Y")
        }
    )
