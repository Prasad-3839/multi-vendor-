from django.db import models
from django.conf import settings

class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.store_name

