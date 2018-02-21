# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

from django.db import IntegrityError
import re
from models import *
import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
	print "index"
	

	return render(request, 'loginregister/index.html')

def success(request):
	print "success"
	try:
		user=User.objects.get(id=request.session['id'])
		context ={ 
			'user': user,
		}
	except User.DoesNotExist:
		return redirect ("/loginregister")		
	return render(request, 'loginregister/success.html', context)

def register(request):	
	print "register"
	if request.method=='POST':
		errors = {}
		errors = User.objects.basic_validator(request.POST) 	
		if(len(errors)):
			for x in errors:
				messages.warning(request, errors[x])
			return redirect('/loginregister')

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		email = request.POST['email'].lower()
		password = request.POST['password']	
		if EMAIL_REGEX.match(request.POST['email']):
			
			hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

			parsed_date = datetime.strptime(request.POST['birthday'], "%Y-%m-%d")
			
			try:
				User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hash1, birthday=parsed_date)

			except IntegrityError as e:
				if 'constraint' in e.message:
					print "ERROR"
				return redirect('/loginregister')			
			request.session['id']=User.objects.get(email=email).id
			
			return redirect('/loginregister/success')
		else:
			print "EMAIL FORM INCORRECt"				 
	return redirect('/loginregister')

def login(request):	
	if request.method=='POST':
		email = request.POST['email'].lower()
		try:
			user = User.objects.get(email=email)
			if(bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
				request.session['id']=user.id
				return redirect('/loginregister/success')
			message.warning(request, 'incorrect username or password')
		except User.DoesNotExist:
			messages.warning(request, 'invalid username or password')
			return redirect ("/loginregister")
	return redirect('/loginregister')			