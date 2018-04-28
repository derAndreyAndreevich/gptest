# coding: utf-8

from django import template
from gptest.models import MenuModel

register = template.Library()

class DrawMenuNode(template.Node):
    _active_item, _dtree, _utree = None, None, None

    def __init__(self, name):
        self._name = name

    @property
    def active_item(self):
        _cn = ".{}.".format(self._name).replace("\"", "")

        self._values = list(MenuModel.objects
            .filter(chain_names__contains=_cn)
            .values_list("id", "parent_id", "name", "title", "url", "has_children"))

        if not self._active_item:
            for it in self._values:
                if it[4] == self._context.get("current_url"):
                    self._active_item = it
                elif it[3] == self._name:
                    self._active_item = it

        return self._active_item

    @property
    def utree(self):
        if not self._utree:
            _list = []
            _stack = [self.active_item[0]]

            while _stack:
                _list.append(_stack.pop())

                for it in self._values:
                    if it[0] == _list[-1]:
                        if it[1]:
                            _stack.append(it[1])

            _list.reverse()
            self._utree = _list

        return self._utree

    @property
    def dtree(self):
        if not self._dtree:
            self._dtree = [it[0] 
                for it in self._values if it[1] == self.active_item[0]]

        return self._dtree

    @property
    def tree(self):
        return self.utree + self.dtree

    def render(self, context):
        self._context = context
        TEMPLATE = \
            "<div style='padding-left: {padding}px'><a href='/{url}'>{has_children}{title}{is_active}</a></div>"

        html = ""
        if self.active_item:
            it = lambda _id: [_it for _it in self._values if _it[0] == _id][0]

            for i, _id in enumerate(self.utree):
                item = it(_id)

                if item[0] == self.active_item[0] and \
                    item[3] == self._context.get("current_url"):
                    is_active_text = "(A)"
                else:
                    is_active_text = ""

                html += TEMPLATE.format(
                    padding=15 * i, 
                    url=item[3],
                    has_children=item[4] and "*" or "",
                    title=item[2],
                    is_active=is_active_text)


            for _id in self.dtree:
                item = it(_id)

                html += TEMPLATE.format(
                    padding=15 * (len(self.utree) + 1), 
                    url=item[3],
                    has_children=item[4] and "*" or "",
                    title=item[2],
                    is_active="")

        return html


@register.tag
def draw_menu(parser, token):
    try:
        tag_name, name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("Format Error")

    return DrawMenuNode(name)