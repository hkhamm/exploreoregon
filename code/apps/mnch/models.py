from django.db import models
from django.template.defaultfilters import slugify

import basic_models
import cachemodel
from ckeditor.fields import HTMLField
from hashlib import md5
import json
from sky_thumbnails.fields import EnhancedImageField
import urlparse

from sky_settings.models import Setting

##
#
# base models
#
##

def _gen_upload_to(instance, filename):
    name = slugify(instance.name)
    if not name:
        name = md5(filename).hexdigest()
    return '%s/%s.png' % (instance.__class__.__name__.lower(), name.lower())

class CategoryModel(basic_models.DefaultModel):
    name = models.CharField(max_length=255, unique=True)
    icon = EnhancedImageField(upload_to=_gen_upload_to, process_source={'size':(64,64)}, help_text='Image should be square and at least 64x64')

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class ResourceModel(basic_models.DefaultModel):
    name = models.CharField(max_length=255)
    url = models.URLField()
    position = models.PositiveIntegerField(default=99, choices=((c,c) for c in range(1,100)))
    class Meta:
        ordering = ('position','name')
        abstract = True

    def __unicode__(self):
        return self.name

    @cachemodel.cached_method
    def favicon_url(self):
        parsed = urlparse.urlparse(self.url)

        try:
            import BeautifulSoup
            import urllib
            page = urllib.urlopen('%s://%s/' % (parsed.scheme, parsed.netloc))
            soup = BeautifulSoup.BeautifulSoup(page)
            link_rel = soup.find("link", rel="shortcut icon")
            if link_rel:
                return link_rel['href']
        except ImportError:
            pass

        return '%s://%s/favicon.ico' % (parsed.scheme, parsed.netloc)


class ApprovedModelManager(basic_models.DefaultModelManager):
    def approved(self):
        return self.filter(status=ApprovedModelMixin.STATUS_APPROVED)

class ApprovedModelMixin(models.Model):
    STATUS_PENDING='pending'
    STATUS_APPROVED='approved'
    STATUS_DENIED='denied'
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_DENIED, "Denied"),
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_APPROVED)
    objects = ApprovedModelManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        auto_approve = Setting.get_value('auto_approve', 0)
        if auto_approve == 1:
            self.status = self.STATUS_APPROVED
        return super(ApprovedModelMixin, self).save(*args, **kwargs)

##
#
# geological sites
#
##


class GeologicalCategory(CategoryModel):
    class Meta:
        verbose_name = 'Go See It Category'
        verbose_name_plural = 'Go See It Categories'

class GeologicalSite(basic_models.DefaultModel):
    category = models.ForeignKey(GeologicalCategory, null=True, blank=True)
    latitude = models.FloatField(help_text="To generate lat/long, use a site like latlong.net")
    longitude = models.FloatField()
    name = models.CharField(max_length=255, unique=True)
    description = HTMLField(blank=False)

    class Meta:
        verbose_name = 'Go See It Sites'
        verbose_name_plural = 'Go See It Sites'

    def __unicode__(self):
        return self.name

    def photos_json(self):
        return json.dumps(list({'name': p.name,
            'url': p.photo.banner.url if p.photo.banner else '',
            'credits': p.credits,
            } for p in self.geologicalsitephoto_set.approved()))


class GeologicalSitePhoto(ApprovedModelMixin, basic_models.DefaultModel):
    site = models.ForeignKey(GeologicalSite)
    name = models.CharField(max_length=255, blank=True)
    photo = EnhancedImageField(upload_to=_gen_upload_to,
        thumbnails={
            'banner':{'size': (900,450),},
            'square':{'size': (300,300),},
        },
        help_text="Image should be at least 900x450 and will be cropped to fit.")
    credits = models.CharField(max_length=255, blank=True)
    position = models.PositiveIntegerField(default=99, choices=((c,c) for c in range(1,100)))

    class Meta:
        ordering = ('position','name')
        verbose_name = 'Go See It Photo'
        verbose_name_plural = 'Go See It Photos'

    def __unicode__(self):
        if self.name:
            return self.name
        if self.credits:
            return self.credits
        return self.photo.name





class GeologicalSiteResource(ResourceModel):
    site = models.ForeignKey(GeologicalSite)


class GeologicalSiteComment(ApprovedModelMixin, basic_models.DefaultModel):
    site = models.ForeignKey(GeologicalSite)
    name = models.CharField(max_length=255)
    body = models.TextField()
    num_likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Go See It Comment'
        verbose_name_plural = 'Go See It Comments'

    def __unicode__(self):
        return '%s\'s comment at %s' % (self.name, self.created_at.strftime('%H:%M on %b %d, %Y'))



##
#
# volunteer opportunities
#
##

class Venue(basic_models.DefaultModel):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(help_text="To generate lat/long, use a site like latlong.net")
    longitude = models.FloatField()
    photo = EnhancedImageField(
        blank=True,
        upload_to=_gen_upload_to,
        thumbnails={
            'banner':{'size': (900,450),},
            'square':{'size': (300,300),},
        },
        help_text="Image should be at least 900x450 and will be cropped to fit."
    )

    def __unicode__(self):
        return self.name


class VolunteerCategory(CategoryModel):
    class Meta:
        verbose_name = 'Go Do It Category'
        verbose_name_plural = 'Go Do It Categories'


class VolunteerOpportunity(basic_models.DefaultModel):
    category = models.ForeignKey(VolunteerCategory, null=True, blank=True)
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    time = models.CharField(max_length=255, blank=True)
    price = models.CharField(max_length=255, blank=True)
    description = HTMLField(blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Go Do It Opportunity'
        verbose_name_plural = 'Go Do It Opportunities'


class VolunteerOpportunityResource(ResourceModel):
    opportunity = models.ForeignKey(VolunteerOpportunity)

