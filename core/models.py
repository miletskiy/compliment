from __future__ import unicode_literals
from django.db import models
from django.conf import settings


class Photo(models.Model):
    """
    Base model for photo objects
    """

    class Meta:
        verbose_name = u"Photo"
        verbose_name_plural = u"Photos"

    title = models.CharField(u"Title", max_length=250, blank=True, null=True)
    description = models.TextField(u"Description", blank=True, default="")
    preview = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True)

    def __unicode__(self):
        return u"{}: {}".format(self.title, self._meta.verbose_name)

    def __str__(self):
        return unicode(self).encode('utf-8')


class UsersPhoto(Photo):
    """
    Model for authenticated users
    """
    class Meta:
        verbose_name = u"UsersPhoto"
        verbose_name_plural = u"UsersPhotos"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

