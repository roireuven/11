# Co nowego w v2.3 / v2.4

Ten przewodnik zawiera podsumowanie głównych funkcji dodanych w **stable v2.3** i **stable v2.4** HotelRestaurantMini-MartManagement.

**Stabilne strony na żywo:**

| Wersja | Adres URL |
|--------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Rozwój** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Pełny interfejs w 21 językach

Interfejs aplikacji internetowej jest dostępny w **21 lokalizacjach**: angielskim, hiszpańskim, francuskim, niemieckim, japońskim, koreańskim, arabskim, hindi, tajskim, wietnamskim, indonezyjskim, tureckim, rosyjskim, włoskim, holenderskim, polskim, hebrajskim, laotańskim, portugalskim (Brazylia), chińskim (uproszczonym) i chińskim (tradycyjnym).

### Gdzie zmienić język

| Ekran | Jak |
|------------|-----|
| **Zaloguj się / skonfiguruj** | Lista języków w nagłówku (przed zalogowaniem) |
| **Po zalogowaniu** | Górny pasek wyboru ustawień regionalnych lub **Lokalizacja** w menu |
| **Ustawienia** | Sekcja języka aplikacji |

Preferencje są zapisywane w pamięci przeglądarki (`hotel_mgr_uiLocale`).

### RTL (od prawej do lewej)

**Arabski** i **Hebrajski** umożliwiają układ RTL dla całej aplikacji. W formularzach modalnych zastosowano ulepszone wyrównanie, dzięki czemu etykiety i dane wejściowe są poprawnie odczytywane zarówno w językach LTR, jak i RTL.

---

## Pierwsza konfiguracja (przetłumaczona)

Kreator instalacji jest w pełni zlokalizowany:

- Nazwa firmy/hotelu
- Tekst nagłówka systemu
- Pola nazwy użytkownika administratora, adresu e-mail i hasła
- Wszystkie przyciski i komunikaty sprawdzające

Po konfiguracji nazwa hotelu jest zapisywana i wyświetlana w nagłówku aplikacji, jeśli została skonfigurowana.

---

## Szybkie akcje w panelu kontrolnym (siatka PMS)

**Panel kontrolny** przedstawia siatkę niebieskich przycisków **+** do typowych zadań:

| Przycisk | Otwiera |
|------------|------------|
| Dodaj pokój | Nowy formularz pokoju |
| Dodaj rezerwację | Nowy formularz rezerwacji |
| Dodaj gościa | Nowy formularz gościa |
| Dodaj zadanie | Nowy bilet konserwacyjny |
| Dodaj usługę | Nowe zgłoszenie serwisowe |
| Dodaj fakturę | Nowy formularz faktury |
| Dodaj zapasy | Nowy przedmiot w ekwipunku |
| Dodaj menu | Nowa pozycja menu |
| Dodaj przedmiot do sklepu | Nowy artykuł w sklepie / mini-martcie |
| Dodaj użytkownika | Nowe konto personelu |

**Uwaga:** *Dodaj czyszczenie* i *Dodaj transakcję* zostały usunięte z tej siatki (wersja 2.4). W razie potrzeby użyj paska bocznego do **sprzątania** i **transakcji**.

---

## Przetłumaczone formy modalne

Okna dialogowe dodawania i edycji są zlokalizowane we wszystkich 21 językach, w tym:

- **Utrzymanie** — nowy bilet (pokój, pierwszeństwo, wydanie, notatki)
- **Faktura** — dodaj/edytuj (gość, pokój, daty, kwoty, status płatności)
- **Inwentarz** – dodaj/edytuj artykuł (nazwa, kod kreskowy, kategoria, ilość, dostępność POS)
- **Pozycja menu** — dodaj / edytuj (nazwa, ikona, cena, kategoria, obraz, link do magazynu)
- **Przechowuj artykuł** — dodaj/edytuj (nazwa, cena, kategoria, ikona półki, kod kreskowy, stan magazynowy)- **Konto użytkownika** — dodaj / edytuj (imię i nazwisko, adres e-mail, hasło, rola)

Etykiety przesyłania obrazów („z urządzenia”, „lub adres URL obrazu”) są zgodne z aktywnym językiem.

---

## Rezerwacja → Nowy gość

Podczas tworzenia **rezerwacji**, jeśli gościa nie ma jeszcze w katalogu:

1. Naciśnij **+ Nowy gość** (lub odpowiednik) w formularzu rezerwacji.
2. Wypełnij moduł **Nowy Gość** (imię i nazwisko, paszport, narodowość, data urodzenia, forma płatności, kontakt, uwagi).
3. Stuknij **Dodaj gościa i wróć** – powracasz do rezerwacji z wybranym nowym gościem.

Selektor narodowości (lista wyszukiwania) jest również przetłumaczony.

---

## Dokumentacja

- Ten przewodnik **Co nowego** jest dostępny we wszystkich 21 językach dokumentacji.
- Otwórz dokumenty w aplikacji: **górny pasek → Dokumentacja**, **☰ Pomoc → Dokumentacja** lub **dolny pasek nawigacyjny → Dokumenty**.
- Samodzielny adres URL: `/doc/?lang={code}#/whats-new-v2`

---

## Dla administratorów

| Zadanie | Gdzie |
|------|------------|
| Szkolenie personelu w zakresie zmiany języka | [Localization](localization.md) |
| Skonfiguruj właściwość po aktualizacji | [Settings & configuration](settings-and-configuration.md) |
| Wdróż aktualizacje | [Deployment](deployment.md) — `npm run deploy:stable` publikuje w wersjach 2.3 i 2.4 |

---

## Powiązane przewodniki

- [Localization](localization.md) — języki, RTL, pliki regionalne
- [First-time setup](first-time-setup.md) — konfiguracja wstępna
- [Navigation & UI](navigation-and-ui.md) — deska rozdzielcza, pasek boczny, nawigacja mobilna
- [Hotel operations](hotel-operations.md) — rezerwacje i goście
- [Deployment](deployment.md) — wersja deweloperska vs stabilna v2.3 / v2.4