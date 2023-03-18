from django.db import models

class sub(models.Model):
	name=models.CharField(max_length=20)
	email=models.CharField(max_length=50,primary_key=True)

class alogin(models.Model):
	Name=models.CharField(max_length=20)
	Pass=models.CharField(max_length=50,primary_key=True)





