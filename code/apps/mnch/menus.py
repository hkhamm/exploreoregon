from client_admin import menus
from client_admin import items

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class MnchMenu(menus.Menu):
    def init_with_context(self, context):
        self.children += [
            items.MenuItem(_('Dashboard'), reverse('admin:index')),

            items.ModelList(
                _('Go See It'),
                models=('mnch.models.GeologicalCategory','mnch.models.GeologicalSite','mnch.models.GeologicalSiteComment'),
            ),

            items.ModelList(
                _('Go Do It'),
                models=('mnch.models.VolunteerCategory','mnch.models.Venue','mnch.models.VolunteerOpportunity'),
            ),

            items.ModelList(
                _('Admin'),
                models=('django.contrib.*','sky_redirects.*','sky_settings.models.Setting','app_log.*')
            ),

            items.Bookmarks(),
            items.MenuItem(
                _('Account'),
                css_classes=('user-tools',),
                children=(
                    items.MenuItem( _('Change password'), reverse('admin:password_change') )
                    , items.MenuItem( _('Log out'), reverse('admin:logout') )
                ),
            ),
        ]
        for child in self.children:
            child.init_with_context(context)


