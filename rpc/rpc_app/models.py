from django.db import models

# Create your models here.
class Flag(models.Model):
	flag = models.CharField(max_length=100)
