from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Corso, Utente, Giorno, Fascia, Aula, Approvazione, Categoria
from .forms import CreaCorso
from . import methods

@login_required(login_url='/login/')
def home(request):
	giorni = Giorno.objects.all()
	categorie = Categoria.objects.all()
	u = Utente.objects.get(user=request.user)
	approvazioni = Approvazione.objects.filter(studente=u).filter(approva=False)
	return render(request, 'corsi/home.html', {'giorniDellaSettimana': giorni, 'categorieDisponibili': categorie, 'approvazioni': approvazioni, 'giorni': giorni, 'categorie': categorie})

@login_required(login_url='/login/')
def success_view(request, idcorso):
	giorni = Giorno.objects.all()
	categorie = Categoria.objects.all()
	return render(request, 'success.html', {'message': 'operazione effettuata con successo', 'giorni': giorni, 'categorie': categorie})

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
		giorni = Giorno.objects.all()
		categorie = Categoria.objects.all()
		return render(request, 'corsi/crea_corso.html', {'crea_corso_form': form, 'fasce': fasce, 'giorni': giorni, 'categorie': categorie})
	elif request.method == 'POST':
		titolo = request.POST.get("titolo", "")
		descrizione = request.POST.get("descrizione", "")
		is_progressive = request.POST.get("is_progressive", "")
		fasce = request.POST.getlist("fasce[]", "")
		ospiti = request.POST.getlist("ospiti[]", "")
		aula = request.POST.get("aula", "")
		classi = request.POST.getlist("classi[]", "")
		categoria = request.POST.get("categoria", "")
		if is_progressive == 'true':
			is_progressive = True
		else:
			is_progressive = False
		risposta = methods.Corso_Delegate().create_corso(request, titolo, descrizione, is_progressive, fasce, ospiti, aula, classi, categoria)
		return JsonResponse(risposta)

@login_required(login_url='/login/')
def rimuovi_corso(request, idcorso):
	giorni = Giorno.objects.all()
	categorie = Categoria.objects.all()
	utente = Utente.objects.get(user=request.user)
	corso = Corso.objects.get(pk=idcorso)
	response = methods.Corso_Delegate.rimuovi_corso(utente, corso)
	return render(request, 'success.html', {'message': response['message'], 'giorni': giorni, 'categorie': categorie})


@login_required(login_url='/login/')
def accetta_corso(request, idapprovazione):
	approvazione = Approvazione.objects.get(pk=idapprovazione)
	corso = approvazione.corso
	approvazione.approva = True
	studente = Utente.objects.get(user=request.user)
	studente.hosted_courses.add(corso)
	studente.save()
	iscrizione = methods.Corso_Delegate().iscrivi_studente(studente.id, corso.id)
	approvazione.save()
	if Approvazione.objects.filter(corso=corso).filter(approva=False).count() == 0:
		corso.convalidato = True
		corso.save()
	if iscrizione['success']:
		return render(request, 'success.html', {'message': 'Operazione avvenuta con successo', 'giorni': giorni, 'categorie': categorie})
	else:
		return render(request, 'success.html', {'message': 'è avvenuto un errore durante la registrazione', 'giorni': giorni, 'categorie': categorie})

@login_required(login_url='/login/')
def iscrizione(request, idcorso):
	if request.method == 'GET':
		giorni = Giorno.objects.all()
		categorie = Categoria.objects.all()
		corso_iscrizione = Corso.objects.get(pk=int(idcorso))
		return render(request, 'corsi/iscrizione.html', {'corso': corso_iscrizione, 'giorni': giorni, 'categorie': categorie, 'fasce': corso_iscrizione.fasce.all(), 'iscritti': corso_iscrizione.iscritti.count()})
	elif request.method == 'POST':
		id_corso = request.POST.get("id_corso", "")
		if (id_corso == id_corso) == False:
			return JsonResponse({'error': 'internal server error (500).'})
		studente = Utente.objects.get(user=request.user)
		risposta = methods.Corso_Delegate().iscrivi_studente(studente.id, idcorso)
		return JsonResponse(risposta)


#ottimizza e migliora la grafica
@login_required(login_url='/login/')
def rimuovi_iscrizione(request, idcorso):
	corso = Corso.objects.filter(pk=idcorso)
	if corso.count() > 0:
		response = methods.Corso_Delegate.disicrivi_studente(request.user, Corso.objects.get(pk=idcorso))
		if response == False:
			return HttpResponse('Il corso non è stato trovato o non è stato possibile disiscrivervi poichè sei nello staff del corso')
	return redirect('/mieicorsi/')

@login_required(login_url='/login/')
def corsi(request):
	giorni = Giorno.objects.all()
	categorie = Categoria.objects.all()
	corsi = Corso.objects.filter(convalidato=True).filter(full=False)
	return render(request, 'corsi/corsi.html', {'corsi': corsi, 'giorni': giorni, 'categorie': categorie})


@login_required(login_url='/login/')
def miei_corsi(request):
	giorni = Giorno.objects.all()
	categorie = Categoria.objects.all()
	iscrizioni = methods.Corso_Delegate().get_corsi(request)
	fasce = Fascia.objects.all()
	hosted_courses = Utente.objects.get(user=request.user).hosted_courses.all()
	return render(request, 'corsi/miei_corsi.html', {'iscrizioni': iscrizioni, 'fasce': fasce, 'hosted_courses': hosted_courses, 'giorni': giorni, 'categorie': categorie})

@login_required(login_url='/login/')
def filtra_categorie(request, categoria):
	giorni = Giorno.objects.all()
	categorie = Categoria.objects.all()
	corsi = Corso.objects.filter(categoria=Categoria.objects.get(nome=categoria))
	return render(request, 'corsi/corsi.html', {'corsi': corsi, 'giorni': giorni, 'categorie': categorie})

def filtra_giorni(request, giorno):
	giorni = Giorno.objects.all()
	categorie = Categoria.objects.all()
	corsi = Corso.objects.filter(fasce__giorno=Giorno.objects.get(giorno_della_settimana=giorno))
	return render(request, 'corsi/corsi.html', {'corsi': corsi, 'giorni': giorni, 'categorie': categorie})

@login_required(login_url='/login/')
def informazioni(request):
	return render(request, 'corsi/informazioni.html', {})

@login_required(login_url='/login/')
def dettagli(request, idcorso):
	corso = Corso.objects.get(pk=idcorso)
	return render(request, 'corsi/dettagli.html', {'corso': corso, 'fasce': corso.fasce.all(), 'studenti': corso.ospitanti.all(), 'iscritti': corso.iscritti.count()})

@login_required(login_url='/login/')
def appello(request, idcorso):
	corso = Corso.objects.get(pk=idcorso)
	studente = Utente.objects.get(user=request.user)
	if (studente == corso.creatore) == False:
		return render(request, 'success.html', {'message': 'solo il creatore del corso può vedere gli appelli per questioni di privacy'})
	iscritti = corso.iscritti.all()
	return render(request, 'corsi/appelli.html', {'iscritti': iscritti})
