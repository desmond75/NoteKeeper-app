from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from todo.models import Note
import datetime
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.forms import PasswordChangeForm 





context ={'year':datetime.datetime.now().year,}

def home(request):
	
	return render(request, 'todo/home.html', context)

def login_(request):

	return render(request, 'todo/login.html')


@login_required
def dashboard(request):
	'''Dashboard, only users who are login can view 
	   the dashbord'''
	return render(request, 'todo/dashboard.html')

	
def signup(request):
	'''Recieves users information to register a
	   new user '''
	if  request.method == 'GET':
		 return render(request, 'todo/signup.html')

    #Validates form and make sure it submited with data
	elif request.POST.get('firstname') == '' or\
	             request.POST.get('lastname') == '' or \
	                 request.POST.get('email') == '' or\
	                     request.POST.get('password') == '' or\
	                          request.POST.get('username') == '':

	      return render(request, 'todo/signup.html', {'error':'All fields are required'})
	else:
		firstname = request.POST.get('firstname')
		lastname = request.POST.get('lastname')
		email = request.POST.get('email')
		password = request.POST.get('password')
		username = request.POST.get('username')
		try:
			user = User.objects.create_user(username=username, first_name=firstname,\
			      last_name=lastname, email=email, password=password)
			user.save()
			login(request, user)
			return redirect('todo:dashboard')
		except IntegrityError:
			return  render(request, 'todo/signup.html', {'error':'Username already exists'})

	return render(request,'todo/signup.html')



def create_note(request, id):
	'''creating notes by recieving and searching for 
	   for a users id '''
	user2 = User.objects.get(pk=id)
	try: 
		if request.POST.get('title') == '' or\
		        request.POST.get('body') == '':
		    context['error'] = 'All fields are required'
		    return render(request, 'todo/dashboard.html', context)
		else:
			title = request.POST.get('title')
			body = request.POST.get('body')
			time = datetime.datetime.now().date()
			user2.note_set.create(title=title,body=body,time=time)
			return redirect('todo:dashboard')
	except:
		return render(request, 'todo/dashboard.html')
	


def view_note(request, id):
	'''recieves note id and queries database for it,
	   if id is found it means note is available and
	   the note instance is passed into context for 
	   displaying'''
	try:
		note = Note.objects.get(pk=id)
		context['note'] = note
		return render(request, 'todo/view_task.html', context)
	except Note.DoesNotExist:
		return render(request, 'todo/404.html')


def edit(request, id):
	''' if request method is GET we query Note by 
	    the id that is passed and populate the forms
	    with the data for user to edit.If request 
	    method is POST it means the data is being
	    send to the server so  we query the database 
	    again with the id being passed to get note 
	    instance and update the particular note with 
	    the data'''
	if request.method == 'GET':
		try:
			note = Note.objects.get(pk=id)
			context['note'] = note
			return render(request, 'todo/edit.html',context)
		except Note.DoesNotExist:
			#return redirect('todo:view_task')
			return render(request,'todo/404.html')
	else:
		try:
			#Validates form  and ensure form is submitted with data
			if request.POST.get('title') == '' or \
			            request.POST.get('body') == '':
				context['errors'] = 'All fields are required'
				return render(request, 'todo/edit.html', context)
			else:
				title = request.POST.get('title')
				body = request.POST.get('body')
				note = Note.objects.get(pk=id)
				note.title = title
				note.body = body
				note.time = datetime.datetime.now().date()
				note.save()
				#alternative method  for updating this model
				#Note.objects.filter(pk=id).update(title=title, body=body, time=time)
				return redirect('todo:dashboard')


		except (Note.DoesNotExist) :
			#context['errord'] = 'All fields are required'
			return render(request, 'todo/404.html')

		return render(request, 'todo/edit.html')



def delete_note(request, id):
	'''Recieves note id and queries Note
	   for it, if note is found 
	   we call delete on it '''
	try:
		note = Note.objects.get(pk=id)
		context['note'] = note
		note.delete()
		return render(request, 'todo/success.html', context)

	except Exception as e:
		return render(request,'todo/404.html')



def change_password(request):
	'''Using default PasswordChangeForm
	   to update a user password and 
	   also calling update_session_auth_hash
	   so as to update users hash in order not 
	   to logout user when password is change    '''
	if request.mothod == 'POST':
		form = PasswordChangeForm(request.user, request.POST)

		if form.is_valid:
			user = form.save()
			update_session_auth_hash(request,user)
	else:
		form = PasswordChangeForm(request.user)
		context['form'] = form

	return render(request,'registration/password_change_form.html', context)











