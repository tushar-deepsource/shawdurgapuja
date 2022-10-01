from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Videos
from django.utils.translation import gettext_lazy as _

class VideosForm(ModelForm):
    class Meta:
        model = Videos
        fields = "__all__"
    
    def clean(self):
        super().clean()
        if (("youtube.com", "youtu.be", "youtube", "youtu") in self.cleaned_data.get("streamingvideolink")):
                raise ValidationError(_("Please put Facebook Url !"), )
        if (("facebook.com", "fb.watch") in self.cleaned_data.get("streamingvideolink")):
                raise ValidationError(_("Please put YouTube Url !"), )