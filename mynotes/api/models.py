from django.db import models

# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        # return self.body[:50] it can take only 50 characters    

