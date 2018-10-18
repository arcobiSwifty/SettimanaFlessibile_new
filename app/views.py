from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .models import Corso, Utente, Giorno, Fascia


giorni = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì']
categorie = ['Sportivo', 'Film', 'Altro']


def login_page(request):

	if request.method == 'GET':
		return render(request, 'registration/login.html')

	elif request.method == 'POST':
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return JsonResponse({'success': 'true'})
		return JsonResponse({'error': 'password o nome utente sbagliato. Ricontrolla'})

#IMPORTANTE: REMOVE THIS FUNCTION! ONLY FOR TESTING

def create_user(request):
	if request.method == 'GET':
		return render(request, 'registration/create_user.html', {})
	elif request.method == 'POST':
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")
		sezione = request.POST.get("sezione", "")
		classe = request.POST.get("classe", "")
		user_create = User.objects.create_user(username, 'test@example.com', password)
		user = authenticate(username=username, password=password)
		Utente.objects.create(nome=username, user=user, classe=classe, sezione=sezione)
		return JsonResponse({'success': True})

def create_corso(request):
	if request.method == 'GET':
		return render(request, 'registration/crea_corso.html')


@login_required(login_url='/login/')
def home(request):
	return render(request, 'corsi/home.html', {'giorniDellaSettimana': giorni, 'categorieDisponibili': categorie})

@login_required(login_url='/login/')
def iscrizione(request):
	return render(request, 'corsi/iscrizione.html')

@login_required(login_url='/login/')
def corsi(request):
	return -1
