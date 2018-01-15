from django.db import models

class Urls(models.Model):
    url = models.CharField(max_length=2000)
    short_url = models.CharField(max_length=100)
    text_message = models.CharField(max_length=2000)
    click_count = models.IntegerField(default=0)
    add_date = models.DateTimeField()

    def __str__(self):
        return self.url
