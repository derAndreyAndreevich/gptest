# coding: utf-8

from django.contrib import admin
from gptest import forms, models

def _action_delete_menu(_, __, qs):
    [it.delete() for it in qs]

# Можно завернуть в gettext. 
# Но это ведь тестовое задание.
_action_delete_menu.short_description = "Delete"

@admin.register(models.MenuModel)
class MenuAdmin(admin.ModelAdmin):
    form = forms.MenuForm
    actions = [_action_delete_menu]

    def get_actions(self, request):
        actions = super(MenuAdmin, self).get_actions(request)

        if 'delete_selected' in actions: 
            del actions['delete_selected']

        return actions