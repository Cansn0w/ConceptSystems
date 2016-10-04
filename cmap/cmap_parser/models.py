from django.db import models


class Cmap(models.Model):
    csv = models.CharField(max_length=255)
    cxl = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return str((self.csv, self.cxl))
