from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
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
        (_('Live Video of Maa Durga coming from potuapara to Home'),{'fields':('maacomevid',)}),
        (_('Puja Dates'),{'fields':('shashti','saptami','ashtami','sandhi','navami','dashami')}),
        
        (_('Shashti Puja Time'),{'fields':('shashtit','shashtite',)}),
        (_('Saptami Puja Time'),{'fields':('saptamit','saptamite',)}),
        (_('Ashtami Puja Time'),{'fields':('ashtamit','ashtamite',)}),
        (_('Sandhi Puja Time'),{'fields':('sandhit','sandhite',)}),
        (_('Maha Bhog Date and Time'),{'fields':('mahabhog','mahabhogdttime')}),
        (_('Navami Puja Time'),{'fields':('navamit','navamite')}),
        (_('Dashami Puja Time'),{'fields':('dashamit','dashamite',)}),

    )


class VideosAdmin(admin.ModelAdmin):
    list_display = ('streamingvideoheader','streamingplatform','yearmodel','day','live')
    list_filter = ('yearmodel','day','live')
    search_fields = list_display + list_filter + ('streamingvideolink',)
    readonly_fields = ('videoid','usernamefb','facebook_posts')
    list_per_page = 100

    fieldsets = (
        (_('Year'),{'fields':('yearmodel',)}),
        (_('Day'),{'fields':('day',)}),
        (_('Streaming Video Data'),{'fields':('streamingvideoheader','streamingplatform','streamingvideodescription')}),
        (_('Streaming Video Links Data'),{'fields':('streamingvideolink','live',)+readonly_fields})
    )

    ## Custom Actions
    #live
    def make_videos_live(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(
                request,
                'Please select only one video',
                messages.ERROR
            )
        else:
            updated  = queryset.update(live=True)
            
            self.message_user(
                    request, 
                    ngettext(
                    '%d video was succesfully made live',
                    '%d videos were succesfully made live',
                    updated,
                ) % updated, 
                messages.SUCCESS
            )
    make_videos_live.short_description = "Make the selected videos go live"

    #offline
    def make_videos_offline(self, request, queryset):
        updated = queryset.update(live=False)
        self.message_user(request, ngettext(
            '%d video was succesfully made offline',
            '%d videos were succesfully made offline',
            updated,
        ) % updated, messages.SUCCESS)
    make_videos_offline.short_description = "Make the selected videos go offline"

    #Registering the custom actions
    actions = [make_videos_live, make_videos_offline]



class LogEntryAdmin(admin.ModelAdmin):
    def delete_admin_logs(self, request, queryset):
        querysetmsg = queryset.delete()
        
        self.message_user(
                request, 
                ngettext(
                '%d log was successfully deleted.',
                '%d logs were successfully deleted.',
                len(queryset),
            ) % int(len(queryset)), 
            messages.SUCCESS
        )
    delete_admin_logs.short_description = "Delete the selected ADMIN Logs without sticking"

    actions = [delete_admin_logs]



admin.site.unregister(Group)

admin.site.register(Year, YearAdmin)
admin.site.register(Videos, VideosAdmin)
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.site_header = admin.site.site_title = 'Shaw Durga Puja Live'

