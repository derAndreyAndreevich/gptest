# coding: utf-8

from django import template

register = template.Library()

class DrawMenuNode(template.Node):

    def __init__(self, name):
        self._name = name

    def render(self):
        return "<div style='background-color: gray'>%s</div>" % self._name


@register.tag
def draw_menu(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Format Error")

    return DrawMenuNode(name)