from django.db import models
from django.contrib.auth.models import User

class Links(models.Model):
    original_link = models.URLField(max_length=500, unique=True)
    short_link = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    visit_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.original_link
