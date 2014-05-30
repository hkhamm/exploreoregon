from client_admin import dashboards
from client_admin import modules
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse




class MnchDashboard(dashboards.Dashboard):

    def init_with_context(self, context):
        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Admin'),
            models=('django.contrib.*','sky_redirects.*', 'sky_settings.*','app_log.*'),
            enabled=False,
        ))

        self.children.append(modules.ModelList(
            _('Go See It Sites'),
            models=('mnch.models.GeologicalCategory','mnch.models.GeologicalSite'),
            enabled=True,
        ))

        self.children.append(modules.ModelList(
            _('Go Do It Opportunities'),
            models=('mnch.models.VolunteerCategory','mnch.models.Venue','mnch.models.VolunteerOpportunity'),
            enabled=True,
        ))

        self.children.append(modules.LinkList(
            _('Moderation Queues'),
            layout='inline',
            enabled=True,
            collapsible=False,
            children=[
                (_('Moderate Comments'), reverse('admin:mnch_geologicalsitecomment_changelist')+'?status__exact=pending&o=-2'),
                (_('Moderate Photos'), reverse('admin:mnch_geologicalsitephoto_changelist')+'?status__exact=pending&o=-4'),
            ]
        ))

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            #draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('admin:password_change')],
                [_('Log out'), reverse('admin:logout')],
            ]
        ))
        # append a recent actions module
        #self.children.append(modules.RecentActions(_('My Actions'), 5))
        # append an all actions module
        self.children.append(modules.AllRecentActions(
            _('Recent Activity')
            , 10
            , css_classes=('activity',)
        ))
