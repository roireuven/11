# Novità nella v2.3 / v2.4

Questa guida riassume le principali funzionalità aggiunte in **stable v2.3** e **stable v2.4** di HotelRestaurantMini-MartManagement.

**Siti stabili live:**

| Versione | URL |
|---------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Sviluppo** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Interfaccia completa in 21 lingue

L'interfaccia utente dell'app Web è disponibile in **21 lingue**: inglese, spagnolo, francese, tedesco, giapponese, coreano, arabo, hindi, tailandese, vietnamita, indonesiano, turco, russo, italiano, olandese, polacco, ebraico, laotiano, portoghese (Brasile), cinese (semplificato) e cinese (tradizionale).

### Dove cambiare lingua

| Schermo | Come |
|--------|-----|
| **Accesso/configurazione** | Elenco a discesa della lingua nell'intestazione (prima dell'accesso) |
| **Dopo il login** | Selettore locale nella barra superiore o **Localizzazione** nel menu |
| **Impostazioni** | Sezione lingua dell'app |

La preferenza viene salvata nella memoria del browser (`hotel_mgr_uiLocale`).

### RTL (da destra a sinistra)

**Arabo** ed **Ebraico** abilitano il layout RTL per l'intera app. I moduli modali utilizzano un allineamento migliorato in modo che le etichette e gli input vengano letti correttamente sia nei linguaggi LTR che RTL.

---

## Prima configurazione (tradotto)

La procedura guidata di configurazione è completamente localizzata:

- Nome dell'azienda/hotel
- Testo dell'intestazione del sistema
- Campi nome utente amministratore, email e password
- Tutti i pulsanti e i messaggi di convalida

Dopo la configurazione, il nome dell'hotel viene memorizzato e mostrato nell'intestazione dell'app, ove configurato.

---

## Azioni rapide della dashboard (griglia PMS)

La **Dashboard** mostra una griglia di pulsanti blu **+** per le attività comuni:

| Pulsante | Apre |
|--------|--------|
| Aggiungi stanza | Nuovo modulo della stanza |
| Aggiungi prenotazione | Nuovo modulo di prenotazione |
| Aggiungi ospite | Nuovo modulo ospite |
| Aggiungi attività | Nuovo ticket di manutenzione |
| Aggiungi servizio | Nuova richiesta di servizio |
| Aggiungi fattura | Nuovo modulo fattura |
| Aggiungi azioni | Nuovo articolo di inventario |
| Aggiungi Menù | Nuova voce di menu |
| Aggiungi articolo nel negozio | Nuovo oggetto negozio/mini-mart |
| Aggiungi utente | Nuovo conto personale |

**Nota:** *Aggiungi pulizia* e *Aggiungi transazione* sono stati rimossi da questa griglia (v2.4). Utilizza la barra laterale per **Pulizia** e **Transazioni** quando necessario.

---

## Forme modali tradotte

Le finestre di dialogo di aggiunta e modifica sono localizzate in tutte le 21 lingue, tra cui:

- **Manutenzione** — nuovo biglietto (camera, priorità, emissione, note)
- **Fattura**: aggiungi/modifica (ospite, camera, date, importi, stato del pagamento)
- **Inventario**: aggiungi/modifica articolo (nome, codice a barre, categoria, quantità, disponibilità POS)
- **Voce di menu**: aggiungi/modifica (nome, icona, prezzo, categoria, immagine, collegamento stock)
- **Articolo del negozio**: aggiungi/modifica (nome, prezzo, categoria, icona scaffale, codice a barre, stock)- **Account utente**: aggiungi/modifica (nome, email, password, ruolo)

Le etichette di caricamento delle immagini ("dal dispositivo", "o URL dell'immagine") seguono la lingua attiva.

---

## Prenotazione → Nuovo ospite

Quando crei una **prenotazione**, se l'ospite non è ancora nella directory:

1. Tocca **+ Nuovo ospite** (o equivalente) nel modulo di prenotazione.
2. Compila il modulo **Nuovo Ospite** (nome, passaporto, nazionalità, data di nascita, metodo di pagamento, contatto, note).
3. Tocca **Aggiungi ospite e ritorna**: ritorni alla prenotazione con il nuovo ospite selezionato.

Anche il selettore della nazionalità (elenco di ricerca) è tradotto.

---

## Documentazione

- Questa guida alle **Novità** è disponibile in tutte le 21 lingue della documentazione.
- Apri i documenti dall'app: **barra superiore → Documentazione**, **☰ Guida → Documentazione** o **navigazione inferiore → Documenti**.
- URL autonomo: `/doc/?lang={code}#/whats-new-v2`

---

## Per gli amministratori

| Compito | Dove |
|------|--------|
| Formare il personale sul cambio di lingua | [Localization](localization.md) |
| Configura la proprietà dopo l'aggiornamento | [Settings & configuration](settings-and-configuration.md) |
| Distribuire gli aggiornamenti | [Deployment](deployment.md) — `npm run deploy:stable` pubblica su v2.3 e v2.4 |

---

## Guide correlate

- [Localization](localization.md): lingue, RTL, file locali
- [First-time setup](first-time-setup.md) — configurazione iniziale
- [Navigation & UI](navigation-and-ui.md): dashboard, barra laterale, navigazione mobile
- [Hotel operations](hotel-operations.md) — prenotazioni e ospiti
- [Deployment](deployment.md) — sviluppo rispetto a v2.3 / v2.4 stabile