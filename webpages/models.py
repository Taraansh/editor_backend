from django.db import models
from django.db import models
from accounts.models import Profile

# Create your models here.
class Page(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    html_content = models.TextField()
    css_content = models.TextField()
    user_email = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.user_email}"

