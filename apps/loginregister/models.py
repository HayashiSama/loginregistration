  # Inside models.py
from __future__ import unicode_literals
from django.db import models
from datetime import datetime




class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}

		if (postData['birthday']):
			parsed_date = datetime.strptime(postData['birthday'], "%Y-%m-%d")
			if parsed_date > datetime.today():
				errors['birthday'] = "Birthday must be before today"
		else:
			errors['birthday'] = "Birthday must be filled in"

		if len(postData['first_name'])<2:
			errors['first_name'] = "First name should be more than 2 characters"
		if len(postData['last_name'])<2:
			errors['last_name'] = "Last name should be more than 2 characters"			
		if (postData['password'] != postData['passwordconfirm']) :
			errors['password_match'] = "Passwords don't match"
		if len(postData['password'])<8:
			errors['password'] = "Password must be at least 8 characters"

#			
		return errors



class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255, unique=True)
	password = models.CharField(max_length=255)
	birthday = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects=UserManager()



