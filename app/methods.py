from .models import Corso, Utente, Giorno, Fascia, Aula, Approvazione
from django.contrib.auth.models import User


class Corso_Delegate:

    def create_corso(request, titolo, descrizione, progressivo, fasce, ospiti, aula, classi):

        fasce_list = list()
        for fascia in fasce:
            n_giorno = fascia.split(', ')[0]
            giorno = Giorno.objects.get(giorno_della_settimana=n_giorno)
            n_fascia = fascia.split(', ')[1]
            f = Fascia.objects.get(giorno=giorno, fascia=n_fascia)
            fasce_list.append(f)

        cr_obj = request.user
        creatore = Utente.objects.get(user=cr_obj)


        ospiti_list = list()
        for ospite, counter in enumerate(ospiti):
            o_str = ''.join(ospite.split()).lower()
            c_str = classi[counter].lower()
            u = Utente.objects.filter(nome=o_str, classe=c_str[0], sezione=c_str[1])
            if u.count() == 0:
                return {'success': False, 'errors': True, 'error': "Lo studente {0} non esiste o non appartiene alla classe {1}".format(o_str, c_str)}
            u_obj = Utente.objects.get(nome=o_str, classe=c_str[0], sezione=c_str[1])
            for fascia in fasce:
                if u_obj.is_fascia_taken(fascia) == True:
                    return {'error': "Lo studente {0} non può ospitare questo corso perchè durante la fascia: \"{1}\" è ospite di un altro corso".format(o_str, fascia)}
            ospiti_list.append(u_obj)

        for fascia in fasce:
            if creatore.is_fascia_taken(fascia) == True:
                return {'error': "Lo studente {0} non può ospitare questo corso perchè durante la fascia: \"{1}\" è ospite di un altro corso".format(creatore, fascia)}

        a = Aula.objects.get(nome_aula=aula)

        c = Corso(nome=titolo, descrizione=descrizione, is_progressive=progressivo, aula=a, creatore=creatore, convalidato=False)
        c.save()

        if creatore not in ospiti_list:
            ospiti_list = [creatore] + ospiti_list

        for o in ospiti_list:
            c.ospitanti.add(o)
        for f in fasce_list:
            c.fasce.add(f)

        c.save()

        creatore.hosted_courses.add(c)
        creatore.save()

        for o in ospiti_list:
            if (o == creatore) == False:
                approvazione = Approvazione(corso = c, studente=o, approva=False)
                approvazione.save()

        return {'success': True, 'errors': False, 'message': 'Corso creato con successo'}


    def iscrivi_studente(studente_id, corso_id):
        try:
            corso = Corso.objects.get(pk=corso_id)
            corso.iscritti.add(studente)
            corso.save()
            studente = Utente.objects.get(pk=studente_id)
            studente.iscrizioni.add(corso)
            studente.save()
        except:
            return {'error': 'Questo corso non esiste, è possibile che sia stato rimosso nel frattempo'}
