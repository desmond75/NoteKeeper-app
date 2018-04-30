from django.db import models
from django.utils import timezone
# Create your models here.
from django.contrib.auth.models import User



class Note(models.Model):
	title = models.CharField(max_length=70)
	body = models.TextField()
	time = models.DateField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)


	def __str__(self):
		return self.title





