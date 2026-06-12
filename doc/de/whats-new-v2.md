# Was ist neu in v2.3 / v2.4?

Dieser Leitfaden fasst die wichtigsten Funktionen zusammen, die in **stable v2.3** und **stable v2.4** von HotelRestaurantMini-MartManagement hinzugefügt wurden.

**Live-Stallseiten:**

| Version | URL |
|---------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Entwicklung** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Vollständige Benutzeroberfläche in 21 Sprachen

Die Web-App-Benutzeroberfläche ist in **21 Gebietsschemata** verfügbar: Englisch, Spanisch, Französisch, Deutsch, Japanisch, Koreanisch, Arabisch, Hindi, Thailändisch, Vietnamesisch, Indonesisch, Türkisch, Russisch, Italienisch, Niederländisch, Polnisch, Hebräisch, Laotisch, Portugiesisch (Brasilien), Chinesisch (vereinfacht) und Chinesisch (traditionell).

### Wo kann man die Sprache ändern?

| Bildschirm | Wie |
|--------|-----|
| **Anmeldung / Einrichtung** | Sprach-Dropdown in der Kopfzeile (vor der Anmeldung) |
| **Nach dem Login** | Gebietsschemaauswahl in der oberen Leiste oder **Lokalisierung** im Menü |
| **Einstellungen** | Abschnitt „App-Sprache“ |

Die Präferenz wird im Browserspeicher (`hotel_mgr_uiLocale`) gespeichert.

### RTL (von rechts nach links)

**Arabisch** und **Hebräisch** ermöglichen das RTL-Layout für die gesamte App. Modale Formulare verwenden eine verbesserte Ausrichtung, sodass Beschriftungen und Eingaben sowohl in LTR- als auch in RTL-Sprachen korrekt gelesen werden.

---

## Erstmalige Einrichtung (übersetzt)

Der Setup-Assistent ist vollständig lokalisiert:

- Firmen-/Hotelname
- Systemkopfzeilentext
- Felder für Admin-Benutzername, E-Mail-Adresse und Passwort
- Alle Schaltflächen und Validierungsmeldungen

Nach der Einrichtung wird der Hotelname gespeichert und im App-Header angezeigt, sofern konfiguriert.

---

## Dashboard-Schnellaktionen (PMS-Raster)

Das **Dashboard** zeigt ein Raster mit blauen ***** Schaltflächen für häufige Aufgaben:

| Knopf | Öffnet |
|--------|--------|
| Raum hinzufügen | Neue Raumform |
| Buchung hinzufügen | Neues Buchungsformular |
| Gast hinzufügen | Neues Gastformular |
| Aufgabe hinzufügen | Neues Wartungsticket |
| Dienst hinzufügen | Neue Serviceanfrage |
| Rechnung hinzufügen | Neues Rechnungsformular |
| Lagerbestand hinzufügen | Neuer Inventargegenstand |
| Menü hinzufügen | Neuer Menüpunkt |
| Shop-Artikel hinzufügen | Neuer Laden-/Minimarktartikel |
| Benutzer hinzufügen | Neues Mitarbeiterkonto |

**Hinweis:** *Reinigung hinzufügen* und *Transaktion hinzufügen* wurden aus diesem Raster entfernt (v2.4). Verwenden Sie bei Bedarf die Seitenleiste für **Hausverwaltung** und **Transaktionen**.

---

## Übersetzte Modalformen

Die Dialoge zum Hinzufügen und Bearbeiten sind in allen 21 Sprachen lokalisiert, darunter:

- **Wartung** – neues Ticket (Raum, Priorität, Problem, Notizen)
- **Rechnung** – hinzufügen/bearbeiten (Gast, Zimmer, Daten, Beträge, Zahlungsstatus)
- **Inventar** – Artikel hinzufügen/bearbeiten (Name, Barcode, Kategorie, Menge, POS-Verfügbarkeit)
- **Menüpunkt** – hinzufügen/bearbeiten (Name, Symbol, Preis, Kategorie, Bild, Aktienlink)
- **Artikel speichern** – hinzufügen/bearbeiten (Name, Preis, Kategorie, Regalsymbol, Barcode, Lagerbestand)- **Benutzerkonto** – hinzufügen/bearbeiten (Name, E-Mail, Passwort, Rolle)

Bild-Upload-Bezeichnungen („vom Gerät“, „oder Bild-URL“) folgen der aktiven Sprache.

---

## Buchung → Neuer Gast

Beim Erstellen einer **Buchung**, wenn der Gast noch nicht im Verzeichnis ist:

1. Tippen Sie im Buchungsformular auf **+ Neuer Gast** (oder gleichwertig).
2. Füllen Sie das Modal **Neuer Gast** aus (Name, Reisepass, Nationalität, Geburtsdatum, Zahlungsmethode, Kontakt, Notizen).
3. Tippen Sie auf **Gast hinzufügen und zurückkehren** – Sie kehren mit dem ausgewählten neuen Gast zur Buchung zurück.

Die Nationalitätsauswahl (Suchliste) ist ebenfalls übersetzt.

---

## Dokumentation

- Dieser Leitfaden **Was ist neu** ist in allen 21 Dokumentationssprachen verfügbar.
- Öffnen Sie Dokumente über die App: **obere Leiste → Dokumentation**, **☰ Hilfe → Dokumentation** oder **untere Navigation → Dokumente**.
- Eigenständige URL: `/doc/?lang={code}#/whats-new-v2`

---

## Für Administratoren

| Aufgabe | Wo |
|------|--------|
| Schulung des Personals zur Sprachumstellung | [Localization](localization.md) |
| Eigenschaft nach Upgrade konfigurieren | [Settings & configuration](settings-and-configuration.md) |
| Updates bereitstellen | [Deployment](deployment.md) – `npm run deploy:stable` veröffentlicht auf v2.3 und v2.4 |

---

## Verwandte Anleitungen

- [Localization](localization.md) – Sprachen, RTL, Gebietsschemadateien
- [First-time setup](first-time-setup.md) – Erstkonfiguration
- [Navigation & UI](navigation-and-ui.md) – Dashboard, Seitenleiste, mobile Navigation
- [Hotel operations](hotel-operations.md) – Buchungen und Gäste
- [Deployment](deployment.md) – Entwicklung vs. stabile Version 2.3 / Version 2.4