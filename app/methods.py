from .models import Corso, Utente, Giorno, Fascia, Aula, Approvazione, Categoria
from django.contrib.auth.models import User


class Corso_Delegate:


    def iscrivi_studente(self, studente_id, corso_id):
        corso = Corso.objects.get(pk=corso_id)
        if corso.full == True:
            return {'error': 'Il corso selezionato è pieno', 'success': False}
        if corso.iscritti.count() >= corso.aula.capacita:
            return {'error': 'Il corso è pieno...', 'success': False}
        studente = Utente.objects.get(pk=studente_id)
        for fascia in corso.fasce.all():
            if studente.is_fascia_taken(fascia):
                return {'error': 'Non è stato possibile iscriversi al corso poichè alcune fasce erano già occupate.', 'success': False}
        corso.iscritti.add(studente)
        studente.iscrizioni.add(corso)
        corso.save()
        studente.save()
        if corso.iscritti.count() >= corso.aula.capacita:
            corso.full = True
            corso.save()
        return {'success': True}

    def get_corsi(self, request):
        studente = Utente.objects.get(user=request.user)
        fasce = Fascia.objects.all()
        iscrizioni = studente.iscrizioni.all()
        iscrizioni_list = list()
        for fascia in fasce:
            i = iscrizioni.filter(fasce__giorno=fascia.giorno, fasce__fascia=fascia.fascia)
            if i.count() == 0:
                iscrizioni_list.append({'fascia': fascia, 'empty': True, 'titolo': '', 'id': 0})
            else:
                i_c = iscrizioni.get(fasce__giorno=fascia.giorno, fasce__fascia=fascia.fascia)
                iscrizioni_list.append({'fascia': fascia, 'empty': False, 'titolo': i_c.nome, 'id': i_c.id})
        return iscrizioni_list

    def create_corso(self, request, titolo, descrizione, progressivo, fasce, ospiti, aula, classi, categoria):

        fasce_list = list()
        for fascia in fasce:
            n_giorno = fascia.split(',')[0]
            giorno = Giorno.objects.get(giorno_della_settimana=n_giorno)
            n_fascia = fascia.split(',')[1][1:]
            f = Fascia.objects.get(giorno=giorno, fascia=n_fascia)
            fasce_list.append(f)

        cr_obj = request.user
        creatore = Utente.objects.get(user=cr_obj)

        ospiti_list = list()
        for counter, ospite in enumerate(ospiti):
            o_str = ''.join(ospite.split()).lower()
            c_str = classi[counter].lower()
            u = Utente.objects.filter(nome=o_str, classe=c_str[0], sezione=c_str[1])
            if u.count() == 0:
                return {'success': False, 'errors': True, 'error': "Lo studente {0} non esiste o non appartiene alla classe {1}".format(o_str, c_str)}
            u_obj = Utente.objects.get(nome=o_str, classe=c_str[0], sezione=c_str[1])
            for fascia in fasce_list:
                if u_obj.is_fascia_taken(fascia) == True:
                    return {'error': "Lo studente {0} non può ospitare questo corso perchè durante la fascia: \"{1}\" è ospite di un altro corso".format(o_str, fascia)}
            ospiti_list.append(u_obj)

        aula_magna = Aula.objects.get(capacita=100)
        for fascia in fasce_list:
            if creatore.is_fascia_taken(fascia) == True:
                return {'error': "Lo studente {0} non può ospitare questo corso perchè durante la fascia: \"{1}\" è ospite di un altro corso".format(creatore, fascia)}
            if Corso.objects.filter(aula=aula_magna).filter(fasce__giorno=fascia.giorno, fasce__fascia=fascia.fascia).count() > 0:
                return  {'error': "durante la fascia: \"{0}\" l'aula magna è già occupata".format(fascia)}

        a = Aula.objects.get(nome_aula=aula)

        if progressivo == False:
            for fascia in fasce_list:
                c = Corso(nome=titolo, descrizione=descrizione, is_progressive=progressivo, aula=a, creatore=creatore, convalidato=False, categoria=Categoria.objects.get(nome=categoria))
                c.save()
                if creatore not in ospiti_list:
                    ospiti_list = [creatore] + ospiti_list

                if len(ospiti_list) == 1:
                    c.convalidato = True

                c.fasce.add(fascia)
                for o in ospiti_list:
                    c.ospitanti.add(o)
                c.save()

                creatore.hosted_courses.add(c)
                creatore.save()

                for o in ospiti_list:
                    if (o == creatore) == False:
                        approvazione = Approvazione(corso =Corso.objects.get(id=c.id), studente=o, approva=False)
                        approvazione.save()

                self.iscrivi_studente(creatore.id, c.id)

        else:

            c = Corso(nome=titolo, descrizione=descrizione, is_progressive=progressivo, aula=a, creatore=creatore, convalidato=False, categoria=Categoria.objects.get(nome=categoria))
            c.save()

            if creatore not in ospiti_list:
                ospiti_list = [creatore] + ospiti_list

            if len(ospiti_list) == 1:
                c.convalidato = True

            for o in ospiti_list:
                c.ospitanti.add(o)
            for f in fasce_list:
                c.fasce.add(f)

            c.save()

            creatore.hosted_courses.add(c)
            creatore.save()

            for o in ospiti_list:
                if (o == creatore) == False:
                    approvazione = Approvazione(corso =Corso.objects.get(id=c.id), studente=o, approva=False)
                    approvazione.save()

            self.iscrivi_studente(creatore.id, c.id)

        return {'success': True, 'errors': False, 'message': 'Corso creato con successo'}


    def disicrivi_studente(studente, corso):
        if corso.contains_studente(studente):

            if corso.full:
                corso.full = False

            utente = Utente.objects.get(user=studente)
            if utente.is_hosted_course(corso) == False:
                utente.iscrizioni.remove(corso)
                utente.save()

                corso.iscritti.remove(utente)
                corso.save()
                return True
        return False

    def rimuovi_corso(studente, corso):
        if corso.is_creator(studente):
            corso.delete()
            return {'success': True, 'error': False, 'message': 'Operazione effettuata con successo'}
        else:
            return {'success': False, 'error': True, 'message': 'Per rimuovere questo corso, contatta il creatore'}
