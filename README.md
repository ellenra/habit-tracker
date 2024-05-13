# Habit Tracker
Seuraa päivittäisiä elämäntapojasi ja osallistu haasteisiin!

## Ominaisuudet
- Käyttäjän luominen, sisään- ja uloskirjautuminen
- Uusi käyttäjä valitsee tavat, mitä haluaa seurata
- Käyttäjä voi lisätä/poistaa tapoja myös myöhemmin
- Käyttäjä voi merkitä päivittäiseen kalenterinäkymään, mitkä tavat suoritettu minäkin päivänä
- Käyttäjä voi seurata suorituksia kuukausittaisesta näkymästä
- Käyttäjä voi osallistua haasteisiin ja luoda haasteita, joihin muut voi osallistua
- Käyttäjä voi seurata haasteissa suoriutumista

## Käynnistysohjeet
1. Kloonaa tämä repositorio ja siirry sen juurihakemistoon
   
   ```
   $ git clone git@github.com:ellenra/habit-tracker.git
   $ cd habit-tracker
   ```
3. Luo sovellukselle PostgreSQL-tietokanta ja kopioi tiedoston schema.sql sisältö tietokantaan, esim.
   
   ```
   $ createdb habittracker
   $ psql habittracker < schema.sql
   ```
5. Luo ja aktivoi virtuaaliympäristö
   
   ```
   $ python3 -m venv venv
   $ source venv/bin/activate
   ```
7. Luo juurihakemistoon .env -tiedosto ja määritä sen sisältö seuraavanlaiseksi
   
   ```
   DATABASE_URL=<tietokannan-osoite>
   SECRET_KEY=<salainen-avain>
    ```
9. Asenna sovelluksen riippuvuudet
    
   ```
   $ pip install -r ./requirements.txt
   ```
11. Nyt sovelluksen voi käynnistää komennolla
    
   ```
   $ flask run
   ```
