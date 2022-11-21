import datetime
import pymongo
from geopy.geocoders import Nominatim
from bson.son import SON


class MongoDB():
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(host='localhost',port=27017)
            self.db = self.client.ProjectMongo
        except Exception as e:
            print(f'Errore di connessione a MongoDB \n{e}')

    def _ricercaBiglietti(self):
        filtri_ricerca = ['artista','genere']
        print("RICERCA dei biglietti \n")
        print('Premi invio per saltare il filtro')
        filtro_utente = [{"biglietti.disponibili": {"$gt":0}}]
        i = 0
        while i<2:
            scelta_utente = input(f'Inserisci {filtri_ricerca[i]} >> ').lower().strip()
            if scelta_utente == "":
                i+=1
            elif scelta_utente not in self.db.concerti.distinct(filtri_ricerca[i]):
                print(f"{filtri_ricerca[i]} non presente nel Database dei concerti")
            else:
                filtro_utente.append({filtri_ricerca[i]:scelta_utente})
        nome_concerto = input(f'Inserisci il nome del concerto >> ').lower().strip()
        if nome_concerto != "":
            filtro_utente.append({"nome_concerto": nome_concerto})
        price = input(f'Inserisci prezzo massimo >> ').strip()
        if price != "":
            filtro_utente.append({"biglietti.prezzo": {"$lte":float(price)}})
        data_iniziale = input('Inserisci la data iniziale (YYYY-MM-DD) >> ')
        if data_iniziale != "":
            filtro_utente.append({"data e ora": {"$gte":datetime.datetime.strptime(data_iniziale,'%Y-%m-%d')}})
            data_finale = input('Inserisci la data finale (YYYY-MM-DD) >> ')
            if data_finale != "":
                filtro_datafinale = datetime.datetime.strptime(data_finale, '%Y-%m-%d') + datetime.timedelta(days=1)
                filtro_utente.append({"data e ora": {"$lte": filtro_datafinale}})
        indirizzo = input('Inserisci il tuo indirizzo >> ').strip()
        if indirizzo != "":
            geolocator = Nominatim(user_agent="Gruppo_migliore")
            location = geolocator.geocode(indirizzo)
            longitudine = location.longitude
            latitudine = location.latitude
            max_dist = float(input('Inserisci la distanza massima (metri) >> '))
            self.db.concerti.create_index([("geometry", pymongo.GEOSPHERE)])
            geofilter = {'loc': {'$near': SON([('$geometry', SON([('type', 'Point'),
                        ('coordinates', [latitudine, longitudine])])),
                        ('$maxDistance', max_dist)])}}
            filtro_utente.append(geofilter)
        filtro_query = {'$and':filtro_utente}
        project_query = {"biglietti.totali":0, "_id":0, "loc":0}
        print("\n\nBiglietti trovati con i filtri indicati:")
        for elem in self.db.concerti.find(filtro_query,project_query):
            print()
            for sub_elem in elem:
                print(f"{sub_elem} >> {elem[sub_elem]}")

    def _acquistoBiglietti(self):
        print("ACQUISTO dei biglietti \n")
        while True:
            print('Inserisci 0 per tornare al Menu')
            idConcerto = int(input('Inserisci codice del concerto >>: '))
            if idConcerto == 0:
                self.menu()
                break
            ids = self.db.concerti.distinct("codice")
            if idConcerto in ids:
                break
            else:
                print('Errore, il codice inserito non corrisponde a nessun concerto \nRiprova!\n')
        while True:
            tot_disp = self.db.concerti.find({"codice": idConcerto}, {"biglietti": 1, "_id": 0})
            disponibili = tot_disp[0]['biglietti']['disponibili']
            print(f'\n{disponibili} biglietti disponibili')
            print()
            nbiglietti = int(input('Inserisci numero di biglietti da acquistare >>: '))
            if nbiglietti <= disponibili:
                break
            else:
                print('Errore, il numero di biglietti inserito è superiore a quelli attualmente disponibili')
        print(f'\nAcquisto di {nbiglietti} biglietto/i effettuato con successo!')
        biglietti_rimasti = disponibili - nbiglietti
        self.db.concerti.update_one({"codice":idConcerto},{"$set": {"biglietti.disponibili":biglietti_rimasti}})


    def menu(self):
        print("BENVENUTO!")
        try:
            while True:
                azioneUtente = int(input('\n\nMENU \n0. Terminare programma \n1. Ricerca dei biglietti \n'
                                         '2. Acquistare biglietti \n  >>: '))
                print()
                if azioneUtente == 0:
                    print('ARRIVEDERCI!')
                    break
                elif azioneUtente == 1:
                    self._ricercaBiglietti()
                elif azioneUtente == 2:
                    self._acquistoBiglietti()
                else:
                    print('Errore, il numero inserito non corrisponde a nessuna operazione \nRiprova!')
        except Exception as err:
            print(f'Errore, comando non valido \n {err}')


def __str__(self):
        return 'Programma per gestire i biglietti dei concerti'



if __name__ == '__main__':
    mongodb = MongoDB()
    mongodb.menu()
