# Program do nauki języków obcych

Krótki opis projektu: Program służy do nauki obcych języków, pomaga rozwiązywać problemy z zapamiętywaniem słówek i jest przeznaczony dla każdego, kto chce efektywnie uczyć się nowego języka.

## Technologie

- `Python 3.11`: Język programowania.
- `SqlAlchemy`: Biblioteka do mapowania obiektowo-relacyjnego.
- `Tkinter`: Biblioteka do tworzenia interfejsu użytkownika.
- `SQLite`: Baza danych.
- `SM2`: Algorytm powtórek.

## Wzorce projektowe

- DTO (Data Transfer Object): Umożliwia przenoszenie danych między procesami.
- Repozytorium: Abstrahuje dostęp do danych.
- Obserwator: Implementuje wzorzec publikuj/subskrybuj, informując obiekty o zmianach w innych obiektach.
- Entity: Reprezentuje obiekty domenowe.

## Struktura projektu

- `main.py`: Plik uruchomieniowy.
- `database.py`: Konfiguracja bazy danych.
- `DTO`: Obiekty Data Transfer Object.
- `Repository`: Abstrakcja dostępu do danych.
- `Validator`: Walidacja danych wejściowych.
- `Entity`: Obiekty domenowe.
- `Enum`: Typy wyliczeniowe.
- `Observer`/`Observable`: Implementacja wzorca obserwatora.
- `View`: Warstwa prezentacji.

## Zadanie techniczne

Stwórz program do nauki obcych słówek. Program powinien umożliwiać zarządzanie kontami użytkowników (każdy użytkownik ma swoje konto zabezpieczone hasłem, na którym przechowywane są jego postępy). Program powinien oferować interfejs tekstowy, przez który użytkownik może wskazać plik ze słówkami do nauki. Następnie program importuje dane i wprowadza je do słownika. W kolejnym kroku program przepytywuje użytkownika z zawartości pliku ze słówkami. Program powinien określać, po ilu dniach użytkownik powinien powtórzyć materiał - jeśli odpowiedział poprawnie, po 7 dniach; jeśli błędnie, od razu. Program tworzy nowy plik z informacjami o dacie ostatniej sesji nauki, ID przyswojonych słówek oraz terminie kolejnej powtórki. Dodatkowo program ma importować log z poprzedniej sesji, aby odpytywać użytkownika z zaplanowanej powtórki. Projekt powinien wykorzystywać wszystkie poznane mechanizmy programistyczne.

## Notatki do realizacji

- Zdecydowałem się napisać aplikację z GUI, a nie CLI, ponieważ jest to bardziej przyjazne dla użytkownika i było dla mnie interesujące napisać aplikację z GUI, ponieważ nigdy wcześniej tego nie robiłem.
- W zadaniu była opisana bardzo prosta logika powtórek, ale ja zdecydowałem się na zaimplementowanie algorytmu SM2, który jest używany w aplikacji Anki, z której korzystam codziennie do nauki języków obcych.
- Ponieważ napisałem aplikację z GUI, zdecydowałem się nie używać plików, tylko bazę danych SQLite, ponieważ jest to bardziej wygodne. Wszystkie informacje, które miały być zapisane w plikach, są zapisane w bazie danych i są dostępne w aplikacji.
- W aplikacji zaimplementowałem system logowania, który jest zabezpieczony hasłem. Hasło jest przechowywane w bazie danych jako hash, i każdy użytkownik ma swoje konto, na którym przechowywane są jego postępy.
- Zdecydowałem się na zaimplementowanie wzorców projektowych, takich jak DTO, Repository, Entity, Validator, Enum, Observer/Observable. Jednak z powodu tego, że implementacja niektórych wzorców projektowych jest skomplikowana, nie zaimplementowałem wszystkich wzorców, które chciałem, ponieważ taka mała aplikacja nie potrzebuje bardzo zaawansowanej struktury. Teraz omówię niektóre z nich:
  - W klasie Database zaimplementowałem wzorzec Singleton. Wzorzec Singleton zapewnia, że klasa ma tylko jedną instancję i zapewnia globalny punkt dostępu do tej instancji. W moim przypadku jest to instancja bazy danych, która jest używana w całej aplikacji. Nie lubię używać tego wzorca, ponieważ jest to antywzorzec. Lepiej używać DI, ale w tym przypadku to dobre rozwiązanie, ponieważ jest to mała aplikacja, a implementacja DI jest skomplikowana.
  - W klasie Repository zaimplementowałem wzorzec Repository. Wzorzec Repository to warstwa abstrakcji dostępu do danych. W moim przypadku jest to warstwa abstrakcji dostępu do bazy danych. Wzorzec Repository zapewnia, że aplikacja nie zależy od konkretnego sposobu dostępu do danych. W moim przypadku jest to baza danych SQLite, ale jeśli kiedyś będę chciał zmienić bazę danych, to nie muszę zmieniać kodu w całej aplikacji, tylko muszę zmienić kod w klasie Repository. Mam też abstrakcyjną klasę generyczną Repository, która jest używana jako interfejs dla klas Repository, które są używane w aplikacji, i zmniejsza duplikację kodu.
  - W klasach Observer/Observable zaimplementowałem wzorzec Observer/Observable. Wzorzec Observer to wzorzec projektowy, który pozwala na stworzenie mechanizmu subskrypcji, gdzie obiekty są powiadamiane o zmianach w innych obiektach. W moim przypadku jest to zaimplementowane dla aktualizacji interfejsu użytkownika. W mojej implementacji jest tylko jeden interfejs update, który przyjmuje jakiekolwiek dane. Lepiej byłoby stworzyć klasę Event, która zawierałaby dane, które są walidowane, ale zdecydowałem się na taką implementację, ponieważ jest to mała aplikacja.
  - Mam też Validatory, które są podobne do Validatorów w Symfony. Ale zrobiłem ich implementację bardzo prostą, ponieważ nie było potrzeby implementować bardziej zaawansowanej walidacji.
  - Też uważam, że plik main można podzielić na mniejsze pliki, ale zdecydowałem się na taką implementację.

## Korzystanie z aplikacji
- Po uruchomieniu aplikacji użytkownik musi się zalogować, lub zarejestrować nowe konto.
- Po zalogowaniu użytkownik musi stworzyć grupę słówek, do której będzie dodawał słówka.
- Po stworzeniu grupy użytkownik może dodać słówka do grupy.
- Po dodaniu słówek użytkownik może zacząć naukę. W trakcie nauki użytkownik będzie przepytywany z wybranych słówek.
- Po zakończeniu nauki użytkownik może zobaczyć swoje postępy.
- Użytkownik może też redagować i usuwać swoje słówka i grupy.
- Żeby zobaczyć przyciski dla redagowania i usuwania użytkownik musi kliknąć na grupę lub słówko prawym przyciskiem myszy.

## Uruchomienie projektu

1. Zainstaluj wymagane zależności przy pomocy `pip install -r requirements.txt`.
2. Uruchom program komendą `python main.py`.
3. Postępuj zgodnie z instrukcjami wyświetlanymi w interfejsie tekstowym.


## Autor

- Yurii Sysoiev
