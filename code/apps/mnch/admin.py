from django.contrib import admin
from client_admin.admin import ClientModelAdmin, TabularInline, StackedInline, GroupedInline

from mnch.models import *
from mnch.forms import *

from sky_thumbnails.fields import EnhancedImageField
from client_admin.widgets import ThumbnailImageWidget
import os

##
#
# category models
#
##

class CategoryAdmin(ClientModelAdmin):
    fieldsets = (
        (None, {'fields': ('name','icon')}),
        ('Meta', {'fields': ('is_active','created_by','updated_by'), 'classes': ('collapse',)}),
    )

admin.site.register(GeologicalCategory, CategoryAdmin)
admin.site.register(VolunteerCategory, CategoryAdmin)




class MyImageWidget(ThumbnailImageWidget):
    def __init__(self, *args, **kwargs):
        self.thumbnail_name = kwargs.pop('preview_thumbnail','thumbnail')
        super(MyImageWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if self.thumbnail_name and value and value.name:
            dirn = os.path.dirname(value.name)
            filen,fileext = os.path.splitext(os.path.basename(value.name))
            value.name = '%s/thumbs/%s.%s%s' % (dirn, filen, self.thumbnail_name, fileext)
        return super(MyImageWidget, self).render(name, value, attrs=attrs)

##
#
# geological site
#
##
class GeologicalCommentInline(StackedInline):
    model = GeologicalSiteComment
    fields = ('status','name','body')
    verbose_name_plural = 'Comments'
    collapse = True

class GeologicalPhotoInline(StackedInline):
    model = GeologicalSitePhoto
    fields = ('status','photo','name','credits','position')
    verbose_name_plural = 'Photos'
    collapse = True
    form = GeologicalSitePhotoForm
    formfield_overrides = {
        EnhancedImageField: {'widget': MyImageWidget(preview_thumbnail='banner')},
    }


class GeologicalResourceInline(StackedInline):
    model = GeologicalSiteResource
    fields = ('name','url','position')
    verbose_name_plural = 'Resources'
    collapse = True


class GeologicalSiteAdmin(ClientModelAdmin):
    inlines = [GeologicalResourceInline, GeologicalPhotoInline, GeologicalCommentInline]
    form = GeologicalSiteForm
    fieldsets = (
        (None, {'fields': ('category','name','latitude','longitude','mapbox','description')}),
        ('Meta', {'fields': ('is_active','created_by','updated_by'), 'classes': ('collapse',)}),
    )
    pass

admin.site.register(GeologicalSite, GeologicalSiteAdmin)

##
#
# image approval queue
#
##
class GeologicalPhotoAdmin(ClientModelAdmin):
    list_display = ('banner_image','name','credits','created_at','site','status')
    raw_id_fields = ('site',)
    list_filter = ('status','created_at')
    fieldsets = (
        (None, {'fields': ('status','site','photo','name','credits')}),
    )
    actions = ('action_approve','action_deny',)
    def action_approve(self, request, queryset):
        queryset.update(status=GeologicalSiteComment.STATUS_APPROVED)
    action_approve.short_description = "Approve selected photos"
    def action_deny(self, request, queryset):
        queryset.update(status=GeologicalSiteComment.STATUS_DENIED)
    action_deny.short_description = "Deny selected photos"

    def banner_image(self, obj):
        return '<img style="width: 200px; height: auto" src="%s"/>' % (obj.photo.banner.url,)
    banner_image.allow_tags = True


admin.site.register(GeologicalSitePhoto, GeologicalPhotoAdmin)

##
#
# comment approval queue
#
##
class GeologicalCommentAdmin(ClientModelAdmin):
    list_display = ('name','created_at','site','status')
    raw_id_fields = ('site',)
    list_filter = ('status','created_at')
    fieldsets = (
        (None, {'fields': ('status','site','name','body')}),
    )
    actions = ('action_approve','action_deny',)
    def action_approve(self, request, queryset):
        queryset.update(status=GeologicalSiteComment.STATUS_APPROVED)
    action_approve.short_description = "Approve selected comments"
    def action_deny(self, request, queryset):
        queryset.update(status=GeologicalSiteComment.STATUS_DENIED)
    action_deny.short_description = "Deny selected comments"

admin.site.register(GeologicalSiteComment, GeologicalCommentAdmin)

##
#
# volunteer opportunities
#
##
class VenueAdmin(ClientModelAdmin):
    form = VenueForm
    fieldsets = (
        (None, {'fields': ('name', 'latitude', 'longitude', 'mapbox', 'address','city','state','zipcode','photo')}),
        ('Meta', {'fields': ('is_active','created_by','updated_by'), 'classes': ('collapse',)}),
    )

admin.site.register(Venue, VenueAdmin)


class VolunteerResourceInline(StackedInline):
    model = VolunteerOpportunityResource
    fields = ('name','url','position')
    verbose_name_plural = 'Resources'
    collapse = True


class VolunteerAdmin(ClientModelAdmin):
    list_display = ('name','date')
    inlines = [VolunteerResourceInline]
    raw_id_fields = ('venue',)
    fieldsets = (
        (None, {'fields': ('category','venue','name', 'date','time','price','description')}),
        ('Meta', {'fields': ('is_active','created_by','updated_by'), 'classes': ('collapse',)}),
    )

admin.site.register(VolunteerOpportunity, VolunteerAdmin)
