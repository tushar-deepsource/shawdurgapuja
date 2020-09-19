from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import Videos, Year


# Register your models here.
class YearAdmin(admin.ModelAdmin):
    list_display = ('year','shashti','saptami','ashtami','sandhi','navami','dashami')
    list_filter = ('year',)
    search_fields = list_display + ('yeardesc',)
    list_per_page = 30

    fieldsets = (
        (_('Year'),{'fields':('year',)}), 
        (_('Year Description'),{'fields':('yeardesc',)}),
        (_('Pictures of Background'),{'fields':('yearpic','colourback','colourtext')}),
        (_('Puja Dates'),{'fields':('shashti','saptami','ashtami','sandhi','navami','dashami')}),
        
        (_('Shashti Puja Time'),{'fields':('shashtit','shashtite',)}),
        (_('Saptami Puja Time'),{'fields':('saptamit','saptamite',)}),
        (_('Ashtami Puja Time'),{'fields':('ashtamit','ashtamite',)}),
        (_('Sandhi Puja Time'),{'fields':('sandhit','sandhite',)}),
        (_('Navami Puja Time'),{'fields':('navamit','navamite')}),
        (_('Dashami Puja Time'),{'fields':('dashamit','dashamite',)}),
        
        (_('Puja Schedule'),{'fields':('pujadatetime',)}),
        (_('Puja Photo'),{'fields':('maadurgaphoto',)})

    )


class VideosAdmin(admin.ModelAdmin):
    list_display = ('streamingvideoheader','streamingplatform','yearmodel','day')
    list_filter = ('yearmodel','day')
    search_fields = list_display + list_filter + ('streamingvideolink',)
    readonly_fields = ('videoid','usernamefb','facebook_posts')
    list_per_page = 100

    fieldsets = (
        (_('Year'),{'fields':('yearmodel',)}),
        (_('Day'),{'fields':('day',)}),
        (_('Streaming Video Data'),{'fields':('streamingvideoheader','streamingplatform','streamingvideodescription')}),
        (_('Streaming Video Links Data'),{'fields':('streamingvideolink','live',)+readonly_fields})
    )



class LogEntryAdmin(admin.ModelAdmin):
    def delete_admin_logs(self, request, queryset):
        querysetmsg = queryset.delete()
        
        self.message_user(
                request, 
                ngettext(
                '%d log was successfully deleted.',
                '%d logs were successfully deleted.',
                len(querysetmsg),
            ) % int(str(int(len(querysetmsg)))), 
            messages.SUCCESS
        )
    delete_admin_logs.short_description = "Delete the selected ADMIN Logs without sticking"

    actions = [delete_admin_logs]



admin.site.unregister(Group)

admin.site.register(Year, YearAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.site_header = admin.site.site_title = 'Shaw Durga Puja Live'
admin.site.index_title = 'Welcome to ShawDurgaPujaLive cPanel'
