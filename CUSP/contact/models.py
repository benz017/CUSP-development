from django.db import models


class Email(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    contact_number = models.CharField(max_length=15)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name