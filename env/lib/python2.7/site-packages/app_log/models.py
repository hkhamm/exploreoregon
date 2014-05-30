from django.db import models


class AppLogManager(models.Manager):
    def log(self, what, **kwargs):
        new_kwargs = {'what': what}
        new_kwargs.update(kwargs)
        entry = self.model(**new_kwargs)
        entry.save()
        return entry

    def log_request(self, request, what, **kwargs):
        new_kwargs = {
            'what': what,
            'who': request.user,
            'where': request.path,
            'ip_address': request.META.get('REMOTE_ADDR',''),
        }
        obj = kwargs.pop('obj',None)
        if obj is not None:
            if hasattr(obj, '_meta'):
                new_kwargs['info'] = u'<%s:%s>' % (obj.__class__.__name__, obj.pk)
            else:
                new_kwargs['info'] = unicode(obj)

        new_kwargs.update(kwargs)
        return self.log(**new_kwargs)

class AppLog(models.Model):
    who = models.CharField(max_length=1024, db_index=True)
    what = models.CharField(max_length=1024, db_index=True)
    when = models.DateTimeField(auto_now_add=True, db_index=True)
    where = models.CharField(max_length=1024, db_index=True)
    info = models.CharField(max_length=1024, blank=True)
    ip_address = models.IPAddressField(blank=True)

    objects = AppLogManager()

    class Meta:
        ordering = ('-when',)

    def __unicode__(self):
        return u"%s %s at %s on %s" % (self.who, self.what, self.where, self.when)








# from mainsite.log import Action

#  AppLog.log(who=request.user, what=LOGGED_IN, where=request.path, ip_address=request.META.REMOTE_ADDR)    

# AppLog.log_request(request, what=LOGGED_IN)
# AppLog.log_request(request, what=LOGGED_IN)


# AppLog.log_request(request, what=UPLOADED_IMAGE, info="image #%s" % (image.pk,))

# AppLog.log_request(request, what=UPLOADED_IMAGE, obj=image)
