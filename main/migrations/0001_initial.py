# Generated by Django 3.1.1 on 2020-10-16 11:53

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import filer.fields.image
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(blank=True, default=django.utils.timezone.now, null=True, unique=True, validators=[django.core.validators.MinValueValidator(2003), main.models.max_value_current_year], verbose_name='Year')),
                ('colourback', colorfield.fields.ColorField(default='rgb(73, 109, 137)', max_length=18, verbose_name='colourback')),
                ('colourtext', colorfield.fields.ColorField(default='#FFF00C', max_length=18, verbose_name='colourtext')),
                ('yeardesc', models.TextField(blank=True, null=True, verbose_name='About the year')),
                ('maacomevid', models.BooleanField(default=True, help_text='Check this checkbox if there will be any video of the Maa coming to home', verbose_name='Will there be any video for the Maa Durga coming to home')),
                ('shashti', models.DateField(blank=True, null=True, verbose_name='Date of Shashti Puja')),
                ('saptami', models.DateField(blank=True, null=True, verbose_name='Date of Saptami Puja')),
                ('ashtami', models.DateField(blank=True, null=True, verbose_name='Date of Ashtami Puja')),
                ('sandhi', models.DateField(blank=True, null=True, verbose_name='Date of Sandhi Puja')),
                ('navami', models.DateField(blank=True, null=True, verbose_name='Date of Navami Puja')),
                ('dashami', models.DateField(blank=True, null=True, verbose_name='Date of Dashami Puja')),
                ('shashtit', models.TimeField(blank=True, null=True, verbose_name='Start Time of Shashti Puja')),
                ('shashtite', models.TimeField(blank=True, null=True, verbose_name='End Time of Shashti Puja')),
                ('saptamit', models.TimeField(blank=True, null=True, verbose_name='Start Time of Saptami Puja')),
                ('saptamite', models.TimeField(blank=True, null=True, verbose_name='End Time of Saptami Puja')),
                ('ashtamit', models.TimeField(blank=True, null=True, verbose_name='Start Time of Ashtami Puja')),
                ('ashtamite', models.TimeField(blank=True, null=True, verbose_name='End Time of Ashtami Puja')),
                ('mahabhog', models.BooleanField(default=False, help_text='Click only when Maha Bhog is organised.', verbose_name='Maha Bhog is there ?')),
                ('mahabhogdttime', models.DateTimeField(blank=True, help_text='Fill this only when "Maha Bhog checkbox" is clicked.', null=True, verbose_name='Maha Bhog Date and Time')),
                ('sandhit', models.TimeField(blank=True, null=True, verbose_name='Start Time of Sandhi Puja')),
                ('sandhite', models.TimeField(blank=True, null=True, verbose_name='End Time of Sandhi Puja')),
                ('navamit', models.TimeField(blank=True, null=True, verbose_name='Start Time of Navami Puja')),
                ('navamite', models.TimeField(blank=True, null=True, verbose_name='End Time of Navami Puja')),
                ('dashamit', models.TimeField(blank=True, null=True, verbose_name='Start Time of Dashami Puja')),
                ('dashamite', models.TimeField(blank=True, null=True, verbose_name='End Time of Dashami Puja')),
                ('maadurgaphoto', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maa_durga_photo', to=settings.FILER_IMAGE_MODEL, verbose_name='Corresponding year Maa Durga Photo')),
                ('maadurgaphoto1', filer.fields.image.FilerImageField(blank=True, help_text='It could be also previous year photo', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='maa_durga_photo_extra', to=settings.FILER_IMAGE_MODEL, verbose_name='Corresponding year Maa Durga Photo Extra')),
                ('yearpic', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='year_back_picture', to=settings.FILER_IMAGE_MODEL, verbose_name='Year Background Image')),
            ],
            options={
                'ordering': ('-year',),
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(blank=True, choices=[('E', 'Ekum'), ('DI', 'Dvitia'), ('T', 'Tritiya'), ('C', 'Maha Chathurti'), ('P', 'Maha Panchami'), ('S', 'Maha Shashti'), ('SA', 'Maha Saptami'), ('A', 'Maha Ashtami'), ('SAN', 'Sandhi Puja'), ('N', 'Maha Navami'), ('D', 'Maha Dashami')], default='S', max_length=50, null=True, verbose_name='Day of Uploading')),
                ('streamingplatform', models.CharField(blank=True, choices=[('F', 'Facebook'), ('Y', 'YouTube')], default='F', max_length=10, null=True, validators=[main.models.validate_platform], verbose_name='Streaming Platform')),
                ('streamingvideoheader', models.CharField(blank=True, max_length=600, null=True, verbose_name='Live Streaming Video Header')),
                ('streamingvideolink', models.URLField(blank=True, null=True, verbose_name='Live Video Link')),
                ('live', models.BooleanField(default=True, help_text='Check this only if the video is live', verbose_name='Live Video')),
                ('videoid', models.CharField(blank=True, max_length=500, null=True, verbose_name='Facebook/YouTube Video ID')),
                ('usernamefb', models.CharField(blank=True, max_length=500, null=True, verbose_name='Facebook User ID')),
                ('embeedlink', models.URLField(blank=True, null=True, verbose_name='Embeed Link of Posts or Video')),
                ('streamingvideodescription', models.TextField(blank=True, help_text='This is optional', null=True, verbose_name='Streaming Video Short Description')),
                ('yearmodel', models.ForeignKey(default=main.models.get_default_year, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.year', verbose_name='Year')),
            ],
            options={
                'verbose_name_plural': 'Videos',
            },
        ),
    ]
