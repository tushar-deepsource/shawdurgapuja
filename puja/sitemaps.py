from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from main.models import Year


class StaticViewSitemap(Sitemap):
    changefreq = 'yearly'

    priority = lambda self, item: 1.0 if item[0] in ('H','s') else 0.80
    
    def items(self):
        year, l = Year.objects.values('year').all() , []
        for i in year: 
            l.extend([f'Videos/{i["year"]}/{day}' for day in ['S','SA','A','SAN','N','D']]+[f'schedule/{i["year"]}'])
        return ['Home'] + l
    
    def location(self, item):
        if item == 'Home':
            return reverse(item)
        elif item[0].lower() == 's':
            return reverse(str(item.split('/')[0]),args=[int(item.split('/')[1])])
        else:
            return reverse(str(item.split('/')[0]),args=[int(item.split('/')[1]),item.split('/')[2]])