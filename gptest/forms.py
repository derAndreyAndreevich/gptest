# coding: utf-8
from django import forms
from gptest.models import MenuModel


class MenuForm(forms.ModelForm):
    CHOICE_NONE = [(0, "This is Root!")]

    parent_id = forms.ChoiceField(required=False)
    name = forms.CharField(required=True)
    title = forms.CharField()
    url = forms.CharField()

    def __init__(self, *args, **kw):
        super(MenuForm, self).__init__(*args, **kw)

        l = lambda _id, name, title: (_id, "%s" % (title,))

        values = MenuModel.objects \
                    .all() \
                    .values_list("id", "chain_names")

        values = [(_id, chain_names[1:-1].replace(".", "->")) 
            for _id, chain_names in values]

        self.fields["parent_id"].choices = \
            [(0, "This is Root!")] + values

    class Meta:
        exclude = ["chain_names", "has_children"]

