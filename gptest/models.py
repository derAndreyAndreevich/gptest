# coding: utf-8
from django.db import models


class MenuModel(models.Model):
    parent_id = models.IntegerField()
    name = models.CharField(unique=True, max_length=255)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    chain_names = models.TextField()
    has_children = models.BooleanField(default=False)

    def save(self, *args, **kw):

        if not self.parent_id:
            self.chain_names = \
                ".%s." % (self.name,)
        else:
            parent = MenuModel.objects.filter(id=self.parent_id).first()
            parent.has_children = True

            self.chain_names = "%s%s." % (parent.chain_names, self.name)

            parent.save()

        super(MenuModel, self).save(*args, **kw)

    def delete(self, *args, **kw):

        MenuModel.objects \
            .filter(chain_names__contains=".%s." % (self.name)) \
            .exclude(id=self.id) \
            .delete()

        super(MenuModel, self).delete(*args, **kw)


    def __str__(self):
        return "%s (%s)" % \
            (self.title, self.chain_names[1:-1].replace(".", "->"))

    class Meta:
        ordering = ["parent_id", "id"]
