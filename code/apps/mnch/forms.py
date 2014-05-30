from django import forms
from django.core.files.images import get_image_dimensions
from django.utils.safestring import mark_safe

from mnch.models import *
from mnch.widgets import MapboxWidget


class GeologicalSiteForm(forms.ModelForm):
    mapbox = forms.CharField(widget=MapboxWidget, required=False)
    class Meta:
        model = GeologicalSite

    def clean(self):
        cleaned_data = super(GeologicalSiteForm, self).clean()
        # Don't allow save without at least one site photo.
        num_site_photos = int(self.data['geologicalsitephoto_set-TOTAL_FORMS'])
        if not num_site_photos:
            num_site_photos = 0
        if num_site_photos < 1:
            from django.core.exceptions import ValidationError
            raise ValidationError('There must be at least one photo for this geological site.')
        return cleaned_data


class VenueForm(forms.ModelForm):
    mapbox = forms.CharField(widget=MapboxWidget, required=False)
    class Meta:
        model = Venue


class GeologicalSitePhotoForm(forms.ModelForm):
    class Meta:
        model = GeologicalSitePhoto

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        w,h = get_image_dimensions(photo)
        if w < 900 or h < 450:
            raise forms.ValidationError("Image must be at least 900x450")
        return photo


class SubmitPhotoForm(GeologicalSitePhotoForm):
    site_id = forms.CharField(required=True)
    class Meta:
        model = GeologicalSitePhoto
        fields = ('name','photo',)


class MobileSubmitPhotoForm(GeologicalSitePhotoForm):
    class Meta:
        model = GeologicalSitePhoto
        fields = ('site','name','photo')


class SubmitCommentForm(forms.ModelForm):
    site_id = forms.CharField(required=True)
    class Meta:
        model = GeologicalSiteComment
        fields = ('name','body',)
