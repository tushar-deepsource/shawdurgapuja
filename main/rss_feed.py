from django.contrib.syndication.views import Feed
from .models import *
from django.urls import reverse_lazy


class YearFeed(Feed):
    title = 'Latest Puja Videos'
    description = 'Get the all the latest puja videos sorted Year-wise'
    link = reverse_lazy('Redirect')

    def get_object(self, request, *args, **kwargs):
        return Year.objects.all()
    

    def title(self, obj):
        return f'YEAR - {obj[0].year}'

    # def link(self, obj):
    #     return obj.get_absolute_url()

    def description(self, obj):
        return obj[0].yeardesc or f'See all the puja videos of the YEAR {obj[0].year}'

    def items(self, obj):
        return Videos.objects.filter(yearmodel=obj[0].id, test=False).order_by('-yearmodel')
    
    def item_copyright(self):
        return 'Copyright (c) 2019, Shaw Durga Puja'
