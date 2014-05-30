import app_log
import json
import re

from django import http
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.forms.models import model_to_dict

from sky_settings.models import Setting

from mnch.models import GeologicalSite, GeologicalSiteComment, GeologicalSitePhoto, VolunteerOpportunity, Venue
from mnch.forms import SubmitPhotoForm, MobileSubmitPhotoForm, SubmitCommentForm
from mnch import actions


def address_passes_whitelist(request_address, whitelist):
    """ just do a simple exact pattern match"""
    return request_address in whitelist


class KioskView(generic.TemplateView):
    template_name = 'index.html'
    def get_context_data(self, *args, **kwargs):
        context = super(KioskView, self).get_context_data(*args, **kwargs)
        geological_sites = GeologicalSite.cached.filter(is_active=True)
        volunteer_opportunities = VolunteerOpportunity.cached.all()

        sites = {}
        for s in geological_sites:
            site = model_to_dict(s)
            site['photos'] = []
            for p in s.geologicalsitephoto_set.approved():
                photo = model_to_dict(p)
                photo['photo'] = p.photo.banner.url if p.photo.banner else ''
                site['photos'].append(photo)
            site['resources'] = []
            for r in s.geologicalsiteresource_set.active():
                resource = model_to_dict(r)
                resource['favicon'] = r.favicon_url()
                site['resources'].append(resource)
            sites[s.pk] = site
        sites_json = json.dumps(sites)

        volunteers = {}
        for v in volunteer_opportunities:
            volunteer = model_to_dict(v)
            volunteer['date'] = volunteer['date'].isoformat()
            volunteer['venue'] = model_to_dict(v.venue)
            volunteer['photo'] = v.venue.photo.banner.url if v.venue.photo else ''
            del volunteer['venue']['photo'] # Remove photos from the array, as they are not JSON serializable
            volunteer['resources'] = []
            for r in v.volunteeropportunityresource_set.active():
                resource = model_to_dict(r)
                resource['favicon'] = r.favicon_url()
                volunteer['resources'].append(resource)
            volunteers[v.pk] = volunteer
        volunteer_json = json.dumps(volunteers)

        # Test if the current ip address is one that should behave like a kiosk
        addresses = Setting.get_value('kiosk_ip_addresses', '')
        whitelist = re.split(r'[,\s]+', addresses)
        passes_whitelist = address_passes_whitelist(self.request.META['REMOTE_ADDR'], whitelist)

        # Optional manual override for testing
        manual_is_kiosk_display = Setting.get_value('is_kiosk_display', False)

        # Set is_kiosk_display if the ip address matches or manual override is set
        is_kiosk_display = False
        if passes_whitelist or manual_is_kiosk_display:
            is_kiosk_display = True

        context.update({
            'mapbox_api_key': Setting.get_value('mapbox_api_key'),
            'session_timeout_hard': Setting.get_value('session_timeout_hard', 120),
            'session_timeout_soft': Setting.get_value('session_timeout_soft', 15),
            'default_location': Setting.get_value('default_location','44.04301, -123.06811').split(','),
            'max_zoom': Setting.get_value('max_zoom', 20),
            'min_zoom': Setting.get_value('min_zoom', 6),
            'southwest_map_boundary': Setting.get_value('southwest_map_boundary', '[38,-138]'),
            'northeast_map_boundary': Setting.get_value('northeast_map_boundary', '[50,-108]'),
            'geological_sites': geological_sites,
            'sites_json': sites_json,
            'volunteer_opportunities': volunteer_opportunities,
            'volunteer_json': volunteer_json,
            'is_kiosk_display': is_kiosk_display,
            'allow_kiosk_commenting': Setting.get_value('allow_kiosk_commenting', True),
            'oregon_border_color': Setting.get_value('oregon_border_color', '#000000'),
        })
        return context


class MobileSubmitPhotoView(generic.CreateView):

    form_class = MobileSubmitPhotoForm
    template_name = 'mobile_submit_photo.html'
    success_url = 'photo_submit_success'

    def form_valid(self, form, *args, **kwargs):
        obj = form.save(commit=False)
        obj.site_id = int(form.data.get('site'))
        obj.name = form.data.get('name','')
        obj.status = obj.STATUS_PENDING
        obj.save()

        app_log.log_request(self.request, actions.SUBMIT_PHOTO, obj=obj)
        return self.render_to_response(self.get_context_data(form=form))


class SubmitGeologicalSitePhotoView(generic.FormView):
    form_class = SubmitPhotoForm
    template_name = 'submit_photo.html'

    def form_valid(self, form, *args, **kwargs):
        obj = form.save(commit=False)
        obj.site_id = int(form.data.get('site_id'))
        obj.credits = form.data.get('your_name','')
        obj.name = form.data.get('description','')
        obj.status = obj.STATUS_PENDING
        obj.save()

        app_log.log_request(self.request, actions.SUBMIT_PHOTO, obj=obj)
        return self.render_to_response(self.get_context_data(form=form))


class SubmitGeologicalSiteCommentView(generic.FormView):
    form_class = SubmitCommentForm
    template_name = 'submit_comment.html'

    def form_invalid(self, form):
        """
        If the form is invalid, do not display any errors (we render them with JS inline)
        """
        pass

    def form_valid(self, form, *args, **kwargs):
        obj = form.save(commit=False)
        obj.site_id = int(form.data.get('site_id'))
        obj.status = obj.STATUS_PENDING
        obj.save()

        app_log.log_request(self.request, actions.SUBMIT_COMMENT, obj=obj)
        return self.render_to_response(self.get_context_data(form=form))


class GeologicalSiteCommentsView(generic.TemplateView):
    template_name = 'comments.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GeologicalSiteCommentsView, self).get_context_data(*args, **kwargs)

        site_id = self.request.REQUEST.get('site_id',None)
        sort = self.request.REQUEST.get('sort','all')

        comments = GeologicalSiteComment.objects.approved().filter(site_id=site_id)
        if sort == 'best':
            comments = comments.order_by('-num_likes')
        else:
            comments = comments.order_by('-created_at')
        context.update({
            'comments': comments,
        })
        return context


class LikeCommentView(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            comment_id = int(request.REQUEST.get('comment_id',-1))
            comment = GeologicalSiteComment.objects.get(pk=comment_id)
            comment.num_likes += 1;
            comment.save()

            app_log.log_request(self.request, actions.LIKE_COMMENT, obj=comment)
            return http.HttpResponse("OK")
        except (GeologicalSiteComment.DoesNotExist, ValueError) as e:
            pass
        return http.HttpResponseBadRequest("FAIL")
