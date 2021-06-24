from django.db import models


class Type(models.Model):

    type = models.CharField(max_length=50)
