from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Corso, Utente, Giorno, Fascia, Aula, Approvazione
from .forms import CreaCorso
from . import methods

giorni = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì']
categorie = ['Sportivo', 'Film', 'Altro']


@login_required(login_url='/login/')
def success_view(request, id_corso):
	return HttpResponse('Iscrizione effettuata (rifai la grafica di questa pagina)')

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

def logout_view(request):
	logout(request)
	return redirect('/login/')

#IMPORTANTE: REMOVE THIS FUNCTION! ONLY FOR TESTING
@login_required(login_url='/login/')
def create_user(request):
	if request.method == 'GET':
		return render(request, 'registration/create_user.html', {})
	elif request.method == 'POST':
		username = request.POST.get("username", "")
		password = request.POST.get("password", "")
		sezione = request.POST.get("sezione", "")
		classe = request.POST.get("classe", "")
		if authenticate(username=username, password=password) is None:
			user_create = User.objects.create_user(username, 'test@example.com', password)
		user = authenticate(username=username, password=password)
		Utente.objects.create(nome=username, user=user, classe=classe, sezione=sezione)
		return JsonResponse({'success': True})

@login_required(login_url='/login/')
def create_corso(request):
	if request.method == 'GET':
		form = CreaCorso()
		fasce = Fascia.objects.all()
		return render(request, 'corsi/crea_corso.html', {'crea_corso_form': form, 'fasce': fasce})
	elif request.method == 'POST':
		titolo = request.POST.get("titolo", "")
		descrizione = request.POST.get("descrizione", "")
		is_progressive = request.POST.get("is_progressive", "")
		fasce = request.POST.getlist("fasce[]", "")
		ospiti = request.POST.getlist("ospiti[]", "")
		aula = request.POST.get("aula", "")
		classi = request.POST.getlist("classi[]", "")
		print(classi)
		if is_progressive == 'true':
			is_progressive = True
		else:
			is_progressive = False

		risposta = methods.Corso_Delegate().create_corso(request, titolo, descrizione, is_progressive, fasce, ospiti, aula, classi)
		return JsonResponse(risposta)


@login_required(login_url='/login/')
def home(request):
	u = Utente.objects.get(user=request.user)
	approvazioni = Approvazione.objects.filter(studente=u)
	return render(request, 'corsi/home.html', {'giorniDellaSettimana': giorni, 'categorieDisponibili': categorie, 'approvazioni': approvazioni})

@login_required(login_url='/login/')
def iscrizione(request, idcorso):
	if request.method == 'GET':
		try:
			corso_iscrizione = Corso.objects.get(pk=int(idcorso))
		except:
			return HttpResponseNotFound('<h1>Questo corso non esiste</h1>')
		return render(request, 'corsi/iscrizione.html', {'corso': corso_iscrizione})
	elif request.method == 'POST':
		id_corso = request.POST.get("id_corso", "")
		if (id_corso == id_corso) == False:
			return JsonResponse({'error': 'internal server error (500).'})
		studente = Utente.objects.get(user=request.user)
		risposta = methods.Corso_Delegate().iscrivi_studente(studente.id, idcorso)
		return JsonResponse(risposta)


@login_required(login_url='/login/')
def rimuovi_iscrizione(request, idcorso):
	corso = Corso.objects.get(pk=idcorso)
	if corso.count() > 0:
		response = methods.Corso_Delegate.disicrivi_studente(request.user, corso)
		if response == False:
			return HttpResponse('Il corso non è stato trovato o non è stato possibile disiscrivervi poichè sei nello staff del corso')
	return redirect('/mieicorsi/')

@login_required(login_url='/login/')
def rimuovi_corso(request, idcorso):
	utente = Utente.objects.get(user=request.user)
	corso = Corso.objects.get(pk=idcorso)
	response = methods.Corso_Delegate.rimuovi_corso(utente, corso)
	return render(request, 'success.html', {'message': response['message']})


@login_required(login_url='/login/')
def accetta_corso(request, idapprovazione):
	approvazione = Approvazione.objects.get(pk=idapprovazione)
	studente = Utente.objects.get(user=request.user)
	corso = approvazione.corso
	approvazione.approva = True
	iscrizione = methods.Corso_Delegate.iscrivi_studente_o(studente, corso)
	studente.hosted_courses.add(corso)
	studente.save()
	approvazione.save()
	if Approvazione.objects.filter(corso=corso).filter(approva=True).count() == 0:
		corso.convalidato = True
		corso.save()
	if iscrizione['success']:
		return render(request, 'success.html', {'message': 'Operazione avvenuta con successo'})
	else:
		return render(request, 'success.html', {'message': 'è avvenuto un errore durante la registrazione'})


@login_required(login_url='/login/')
def corsi(request):
	corsi = Corso.objects.all()
	return render(request, 'corsi/corsi.html', {'corsi': corsi})


@login_required(login_url='/login/')
def miei_corsi(request):
	iscrizioni = methods.Corso_Delegate().get_corsi(request)
	fasce = Fascia.objects.all()
	hosted_courses = Utente.objects.get(user=request.user).hosted_courses.all()
	return render(request, 'corsi/miei_corsi.html', {'iscrizioni': iscrizioni, 'fasce': fasce, 'hosted_courses': hosted_courses})
