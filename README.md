# Py-MongoDB
Programma per gestire i biglietti dei concerti, con MongoDB e Python

E' possibile ricercare un concerto in base ai seguenti filtri (anche contemporaneamente):
  1. Artista
  2. Genere
  3. Titolo del concerto
  4. Prezzo massimo
  5. Data 
  6. Distanza dal proprio indirizzo (GeoQuery)

>: I concerti vengono mostrati solamente se sono ancora disponibili dei biglietti
>: per effetturare la GeoQuery, viene richiesto all'utente di inserire un indirizzo e la distanza massima (in metri) tra esso e i concerti disponibili


Per acquistare i biglietti dei concerti bisogna indicare:
  - Codice del concerto
  - Numero di biglietti 


NB. 
MongoDB è un Database NoSQL implementato come un archivio di documenti
La libreria di geocoding utilizzata in questo programma è Geopy
