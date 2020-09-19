import datetime
import os
from random import randint

from colorfield.fields import ColorField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import mark_safe
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField
from filer.models import Image as Images
from PIL import Image, ImageDraw, ImageOps

from .get_username import get_request


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year()+1)(value) 


# Create your models here.
class Year(models.Model):
    '''
    Model to store the Year of Durga Puja live links and its correspondence 
    '''
    year = models.IntegerField(_('Year'),unique=True, null=True,blank=True, default=now,validators=[MinValueValidator(2003), max_value_current_year])
    
    yearpic = FilerImageField(verbose_name='Year Background Image', related_name='year_back_picture',blank=True, null=True, on_delete=models.SET_NULL)
    colourback = ColorField(_('colourback'),default='rgb(73, 109, 137)')
    colourtext = ColorField(_('colourtext'),default='#FFF00C')
    yeardesc = models.TextField(_('About the year'),blank=True, null=True)
    
    shashti = models.DateField(_('Date of Shashti Puja'), blank=True, null=True)
    saptami = models.DateField(_('Date of Saptami Puja'), blank=True, null=True)
    ashtami = models.DateField(_('Date of Ashtami Puja'), blank=True, null=True)
    sandhi = models.DateField(_('Date of Sandhi Puja'), blank=True, null=True)
    navami = models.DateField(_('Date of Navami Puja'), blank=True, null=True)
    dashami = models.DateField(_('Date of Dashami Puja'), blank=True, null=True)

    #Puja Timings
    shashtit = models.TimeField(_('Start Time of Shashti Puja'), blank=True, null=True)
    shashtite = models.TimeField(_('End Time of Shashti Puja'), blank=True, null=True)

    saptamit = models.TimeField(_('Start Time of Saptami Puja'), blank=True, null=True)
    saptamite = models.TimeField(_('End Time of Saptami Puja'), blank=True, null=True)

    ashtamit = models.TimeField(_('Start Time of Ashtami Puja'), blank=True, null=True)
    ashtamite = models.TimeField(_('End Time of Ashtami Puja'), blank=True, null=True)

    sandhit = models.TimeField(_('Start Time of Sandhi Puja'), blank=True, null=True)
    sandhite = models.TimeField(_('End Time of Sandhi Puja'), blank=True, null=True)

    navamit = models.TimeField(_('Start Time of Navami Puja'), blank=True, null=True)
    navamite = models.TimeField(_('End Time of Navami Puja'), blank=True, null=True)

    dashamit = models.TimeField(_('Start Time of Dashami Puja'), blank=True, null=True)
    dashamite = models.TimeField(_('End Time of Dashami Puja'), blank=True, null=True)

    #File and Photos
    pujadatetime = FilerFileField(verbose_name=_('Puja schedule file'), related_name='puja_schedule',help_text='This must be a file a pdf, or an image', blank=True, null=True, on_delete=models.SET_NULL)

    maadurgaphoto = FilerFileField(verbose_name=_('Corresponding year Maa Durga Photo'), related_name='maa_durga_photo', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('-year',)
    
    def __str__(self):
        return f'{self.year}'

    def view_puja_dates_and_time(self):
        '''A button to view the pdf puja schedule file'''
        return mark_safe(f'<a href="pdf/{self.pujadatetime.url}" onclick="return showAddAnotherPopup(this)" class="submit-row">Click Here</a>')


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT)):
            pass
        else: os.mkdir(os.path.join(settings.MEDIA_ROOT))
        #Generating the Image!
        if self.yearpic == None or self.yearpic == "" or self.yearpic == " ":
            #The main image var
            output_image = os.path.join(settings.MEDIA_ROOT, "yearpic", str(self.year) + 'output' +'.png')
            main_image = os.path.join(settings.MEDIA_ROOT, "yearpic", str(self.year) + '.png')
                
            main_imagename = str(self.year) + '.png'

            #IMage initialisation and darwing
            img = Image.new('RGBA', (100, 30), color = str(self.colourback))
            d = ImageDraw.Draw(img)
            w, h = d.textsize(str(self.year))

            d.text(((100-w)/2,(30-h)/2), str(self.year), fill=str(self.colourtext))

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
            #Deleting the first image made
            os.remove(output_image1)

            #Saving the image
            req = get_request().user
            with open(main_image1, "rb") as f:
                file_obj = File(f, name=main_imagename)
                image = Images.objects.create(
                    owner=req,
                    original_filename=main_imagename,
                    file=file_obj
                )
                self.yearpic = image
                
            #Removing the playlist image and playlist folder
            os.remove(main_image1)
            try: os.rmdir(os.path.join(settings.MEDIA_ROOT, "yearpic"))
            except: pass
        
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    def delete(self, using=None, keep_parents=False):
        if os.path.exists(os.path.join(settings.MEDIA_ROOT,str(self.yearpic.url))):
            os.remove(os.path.join(settings.MEDIA_ROOT,str(self.yearpic.url)))
        return super().delete(using=using, keep_parents=keep_parents)


def validate_platform(value):
    if value.upper() == 'Y':
            raise ValidationError(
                _('YouTube streaming is not available! Please Choose the other option'),
            )


def get_default_year():
    from datetime import datetime
    return Year.objects.get_or_create(year=int(datetime.now().strftime("%Y")))

class Videos(models.Model):
    """
    Stores a single Video entry, related to :model:`main.Year`
    according the day of uploading (Maha Shashti, Maha Saptami, Maha Ashtami, Maha Navami, Maha Dashami)
    """
    yearmodel = models.ForeignKey(Year,verbose_name= _('Year'),null=True, default=get_default_year,on_delete=models.SET_NULL)
    day = models.CharField(_('Day of Uploading'),null=True, blank=True,choices=(('S','Maha Shashti'),('SA','Maha Saptami'),('A','Maha Ashtami'),('SAN','Sandhi Puja'),('N','Maha Navami'),('D','Maha Dashami')),max_length=50)
    
    streamingplatform = models.CharField(_('Streaming Platform'),null=True, blank=True,choices=(('F','Facebook'),('Y','YouTube')),max_length=10,default="F",validators=[validate_platform])
    streamingvideoheader = models.CharField(_('Live Streaming Video Header'),null=True,blank=True,max_length=600)
    
    streamingvideolink = models.URLField(_('Live Video Link'), null=True, blank=True)
    live = models.BooleanField(_('Live Video'), help_text=_('Check this only if the video is live'), default=True)
    videoid = models.CharField(_('Facebook/YouTube Video ID'),max_length=500, null=True, blank=True)
    usernamefb = models.CharField(_('Facebook User ID'),max_length=500, null=True, blank=True)
    embeedlink = models.URLField(_('Embeed Link of Posts or Video'),null=True, blank=True)
    
    streamingvideodescription = models.TextField(_('Streaming Video Short Description'), help_text='This is optional', null=True,blank=True)

    
    def __str__(self):
        try:
            aname = self.streamingvideoheader + ' ' +str(Year.objects.values('year').filter(id=self.yearmodel.id).get()['year'] )
        except: aname = "Deleted Year" + " " + self.streamingvideoheader + " " + f'({self.day})'
        return aname
    

    def facebook_posts(self):
        '''This is method to generate the facebook video in an iframe'''
        url = f'https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com%2F{self.usernamefb}%2Fvideos%2F{self.videoid}%2F&show_text=false&width=734&height=504&appId'
        return mark_safe(f'<iframe src="{url}" width="734" height="504" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowTransparency="true" allow="encrypted-media" allowFullScreen="true"></iframe>')
    
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.streamingvideolink[-1] != '/':
            self.streamingvideolink = self.streamingvideolink + '/'
        a = self.streamingvideolink.lstrip('https://www.facebook.com/')
        lista = a.split('/')
        if len(lista) == 4:
            self.videoid = lista[-2]
        elif len(lista) == 3:
            self.videoid = list[-1]
        self.usernamefb = lista[0]
        self.embeedlink = f'https://www.facebook.com/plugins/video.php?href=https%3A%2F%2Fwww.facebook.com%2F{self.usernamefb}%2Fvideos%2F{self.videoid}%2F&show_text=false&width=734&height=504&appId'

        Videos.objects.update(live=False)
        self.live = self.live

        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    
    class Meta:
        verbose_name_plural = "Videos"
