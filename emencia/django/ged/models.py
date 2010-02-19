"""Models for emencia.django.ged"""
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField

class Path(models.Model):
    """Path for ordering documents"""

    name = models.CharField(_('name'), max_length=250)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True,
                               verbose_name=_('path'))
    creator = models.ForeignKey(User, verbose_name=_('creator'))
    creation_date = models.DateTimeField(_('creation_time'), auto_now_add=True)

    def virtual_path(self):
        if self.parent:
            return '%s/%s' % (self.parent.virtual_path(), self.slug)
        return '%s' % self.slug

    def __unicode__(self):
        return '/%s' % self.virtual_path()

    @models.permalink
    def get_absolute_url(self):
        return ('ged_path_browsing', (self.virtual_path() + '/',))

    class Meta:
        ordering = ('name',)
        verbose_name = _('path')
        verbose_name_plural = _('paths')

DOCUMENT_STATUS = ((0, _('draft')),
                   (1, _('published')),
                   (2, _('rejected')),
                   )

class Document(models.Model):
    """Documents"""
    name = models.CharField(_('title'), max_length=250)
    slug = models.SlugField()

    document = models.FileField(_('document'), upload_to='uploads/documents')
    description = models.TextField(_('description'), blank=True)

    language = models.CharField(_('language'), max_length=2, blank=True,
                                choices=settings.LANGUAGES)
    status = models.IntegerField(_('status'), choices=DOCUMENT_STATUS)
    path = models.ForeignKey(Path, blank=True, null=True,
                             verbose_name=_('path'))
    tags = TagField(_('tags'))
    
    creator = models.ForeignKey(User, verbose_name=_('creator'), related_name='creator')
    creation_date = models.DateTimeField(_('creation_time'), auto_now_add=True)
    modifier = models.ForeignKey(User, verbose_name=_('modifier'), related_name='modifier')
    modification_date = models.DateTimeField(_('modification_time'), auto_now=True)

    def virtual_path(self):
        if self.path:
            return '%s/%s' % (self.path.virtual_path(), self.slug)
        return '%s' % self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('ged_path_browsing', (self.virtual_path(),))

    def __unicode__(self):
        return self.name

    def size(self):
        return self.pretty_size(self.document.size)

    def pretty_size(self, size):
        suffixes = [("B", 2**10), ("K", 2**20), ("M", 2**30), ("G", 2**40), ("T", 2**50)]
        for suf, lim in suffixes:
            if size > lim:
                continue
            else:
                return round(size/float(lim/2**10),2).__str__()+suf



    def icon(self):
        return self.document.name.split('.')[-1]

    class Meta:
        ordering = ('name',)
        verbose_name = _('document')
        verbose_name_plural = _('document')
