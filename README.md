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
## Kuvia sovelluksesta

![Screenshot from 2024-05-13 17-29-54](https://github.com/ellenra/habit-tracker/assets/102103873/7c503d67-083f-42d1-815e-3dd0c74c1a09)
![Screenshot from 2024-05-13 17-29-33](https://github.com/ellenra/habit-tracker/assets/102103873/d8c4559f-dbc2-450c-8bef-db130b2af076)
![Screenshot from 2024-05-13 17-44-29](https://github.com/ellenra/habit-tracker/assets/102103873/b1678a98-6b35-473b-ae5e-baa1150cbe9e)
