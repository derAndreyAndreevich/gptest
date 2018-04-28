# coding: utf-8
from django.views.generic.base import TemplateView

class IndexPageView(TemplateView):
    template_name = "base.html"

    def get(self, request, url=None):
        self._url = url

        return super(IndexPageView, self).get(request, url)

    def get_context_data(self, *args, **kw):
        context = super(IndexPageView, self).get_context_data(*args, **kw)

        context["current_url"] = self._url

        return context


