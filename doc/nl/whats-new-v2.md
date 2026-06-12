# Wat is er nieuw in v2.3 / v2.4

Deze handleiding geeft een samenvatting van de belangrijkste functies die zijn toegevoegd in **stable v2.3** en **stable v2.4** van HotelRestaurantMini-MartManagement.

**Live stabiele sites:**

| Versie | URL |
|---------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Ontwikkeling** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Volledige interface in 21 talen

De gebruikersinterface van de webapp is beschikbaar in **21 talen**: Engels, Spaans, Frans, Duits, Japans, Koreaans, Arabisch, Hindi, Thais, Vietnamees, Indonesisch, Turks, Russisch, Italiaans, Nederlands, Pools, Hebreeuws, Laotiaans, Portugees (Brazilië), Chinees (vereenvoudigd) en Chinees (traditioneel).

### Waar taal wijzigen

| Scherm | Hoe |
|--------|-----|
| **Inloggen / instellen** | Vervolgkeuzelijst Taal in de koptekst (vóór inloggen) |
| **Na inloggen** | Landinstellingenkiezer in de bovenste balk of **Lokalisatie** in het menu |
| **Instellingen** | App-taalsectie |

Voorkeur wordt opgeslagen in browseropslag (`hotel_mgr_uiLocale`).

### RTL (van rechts naar links)

**Arabisch** en **Hebreeuws** schakelen de RTL-indeling in voor de hele app. Modale formulieren gebruiken een verbeterde uitlijning, zodat labels en invoer correct worden gelezen in zowel de LTR- als de RTL-taal.

---

## Eerste installatie (vertaald)

De installatiewizard is volledig gelokaliseerd:

- Bedrijfs-/hotelnaam
- Systeemkoptekst
- Velden voor beheerdersgebruikersnaam, e-mailadres en wachtwoord
- Alle knoppen en validatieberichten

Na de configuratie wordt de hotelnaam opgeslagen en weergegeven in de app-header, indien geconfigureerd.

---

## Dashboard snelle acties (PMS-raster)

Het **Dashboard** toont een raster van blauwe **+** knoppen voor algemene taken:

| Knop | Opent |
|--------|--------|
| Kamer toevoegen | Nieuwe kamervorm |
| Boeking toevoegen | Nieuw boekingsformulier |
| Gast toevoegen | Nieuw gastformulier |
| Taak toevoegen | Nieuw onderhoudsticket |
| Dienst toevoegen | Nieuw serviceverzoek |
| Factuur toevoegen | Nieuw factuurformulier |
| Voorraad toevoegen | Nieuw inventarisitem |
| Menu toevoegen | Nieuw menu-item |
| Winkelartikel toevoegen | Nieuw winkel- / mini-martartikel |
| Gebruiker toevoegen | Nieuw personeelsaccount |

**Opmerking:** *Opschoning toevoegen* en *Transactie toevoegen* zijn uit dit raster verwijderd (v2.4). Gebruik indien nodig de zijbalk voor **Huishouden** en **Transacties**.

---

## Vertaalde modale vormen

Dialoogvensters voor toevoegen en bewerken zijn gelokaliseerd in alle 21 talen, waaronder:

- **Onderhoud** — nieuw ticket (kamer, prioriteit, uitgave, opmerkingen)
- **Factuur** — toevoegen/bewerken (gast, kamer, data, bedragen, betalingsstatus)
- **Inventaris** — item toevoegen/bewerken (naam, streepjescode, categorie, aantal, POS-beschikbaarheid)
- **Menu-item** — toevoegen/bewerken (naam, pictogram, prijs, categorie, afbeelding, voorraadlink)
- **Winkelartikel** — toevoegen/bewerken (naam, prijs, categorie, plankpictogram, streepjescode, voorraad)- **Gebruikersaccount** — toevoegen/bewerken (naam, e-mailadres, wachtwoord, rol)

Labels voor het uploaden van afbeeldingen (“van apparaat”, “of afbeeldings-URL”) volgen de actieve taal.

---

## Boeking → Nieuwe gast

Bij het aanmaken van een **boeking** en de gast nog niet in de directory staat:

1. Tik op **+ Nieuwe gast** (of gelijkwaardig) op het boekingsformulier.
2. Vul het formulier **Nieuwe gast** in (naam, paspoort, nationaliteit, geboortedatum, betaalmethode, contact, opmerkingen).
3. Tik op **Gast toevoegen en terugkeren** — u keert terug naar de boeking met de nieuwe gast geselecteerd.

De nationaliteitskiezer (zoeklijst) wordt ook vertaald.

---

## Documentatie

- Deze gids **Wat is er nieuw** is beschikbaar in alle 21 documentatietalen.
- Open documenten vanuit de app: **bovenste balk → Documentatie**, **☰ Help → Documentatie**, of **navigatie onderaan → Documenten**.
- Zelfstandige URL: `/doc/?lang={code}#/whats-new-v2`

---

## Voor beheerders

| Taak | Waar |
|------|--------|
| Train personeel op taalwissel | [Localization](localization.md) |
| Eigenschap configureren na upgrade | [Settings & configuration](settings-and-configuration.md) |
| Updates implementeren | [Deployment](deployment.md) — `npm run deploy:stable` publiceert naar v2.3 en v2.4 |

---

## Gerelateerde handleidingen

- [Localization](localization.md) — talen, RTL, landinstellingsbestanden
- [First-time setup](first-time-setup.md) — initiële configuratie
- [Navigation & UI](navigation-and-ui.md) — dashboard, zijbalk, mobiele navigatie
- [Hotel operations](hotel-operations.md) — boekingen en gasten
- [Deployment](deployment.md) — ontwikkeling vs. stabiel v2.3 / v2.4