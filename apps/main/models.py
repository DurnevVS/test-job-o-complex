from django.db import models
from django.utils.translation import gettext_lazy as _


class Cookie(models.Model):
    sessionid = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Cookie'
        verbose_name_plural = 'Cookies'

    def __str__(self):
        return self.sessionid


class SearchHistory(models.Model):
    cookie = models.ForeignKey(Cookie, on_delete=models.CASCADE, related_name='search_history')
    city = models.CharField(max_length=255, verbose_name=_('Город'))
    lat = models.CharField(max_length=255, verbose_name=_('Широта'))
    long = models.CharField(max_length=255, verbose_name=_('Долгота'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('История поиска')
        verbose_name_plural = _('История поиска')

    def __str__(self):
        return self.city
