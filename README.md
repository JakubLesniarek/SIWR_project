# SIWR_project
# Object Tracking System

System śledzenia obiektów w sekwencjach wideo wykorzystujący algorytm węgierski do optymalnego przypisania obiektów między kolejnymi klatkami.

## Opis

Aplikacja implementuje zaawansowany system śledzenia obiektów, który analizuje sekwencje obrazów i śledzi ruch wykrytych obiektów w czasie. System wykorzystuje algorytm węgierski (Hungarian Algorithm) do rozwiązywania problemu przypisania obiektów między kolejnymi klatkami.

## Funkcjonalności

- **Śledzenie obiektów** - Automatyczne przypisywanie obiektów między klatkami
- **Predykcja ruchu** - Przewidywanie pozycji obiektów na podstawie historii ruchu
- **Ocena podobieństwa** - Analiza wielkości i pozycji obiektów
- **Ewaluacja wyników** - Porównanie z danymi referencyjnymi
- **Eksport wyników** - Zapis rezultatów do pliku tekstowego

## Wymagania
python >= 3.6
numpy
scipy

## Instalacja
pip install numpy scipy

## Struktura danych wejściowych

System oczekuje pliku  bboxes.txt  w następującym formacie:
c6s1_000451.jpg

1

420.836933 144.188985 88.328294 216.466523

c6s1_000476.jpg

3

325.044276 151.653348 126.894168 204.025918

177.001080 160.361771 90.816415 153.019438

129.726782 129.260259 83.352052 195.317495

etc.

Gdzie:
- Pierwsza linia: nazwa pliku obrazu
- Druga linia: liczba obiektów w klatce
- Następne linie: współrzędne obiektów w formacie x,y,width,height
## Użycie

### Podstawowe śledzenie

python main.py /path/to/data/folder


### Śledzenie z oceną dokładności

Jeśli folder zawiera plik bboxes_gt.txt  z danymi referencyjnymi:

System automatycznie wykryje dane referencyjne i wyświetli dokładność śledzenia.

## Parametry konfiguracyjne

- prog_dystansu: Maksymalny dystans dla przypisania obiektów (domyślnie: 50)
- min_podobienstwo: Minimalny próg podobieństwa obszarów (domyślnie: 0.3)

## Algorytm

System wykorzystuje następujące komponenty:
## Algorytm śledzenia - krok po kroku

### 1. Wczytanie danych
- System wczytuje plik  bboxes.txt  z pozycjami obiektów w każdej klatce
- Sortuje klatki według numerów (wyciąganych z nazw plików)
- Przygotowuje struktury do przechowywania historii ruchu

### 2. Przetwarzanie pierwszej klatki
- Dla pierwszej klatki wszystkie obiekty otrzymują ID = -1 (nowe obiekty)
- Nie ma jeszcze historii ruchu do analizy

### 3. Przetwarzanie kolejnych klatek
Dla każdej kolejnej klatki system wykonuje następujące kroki:

#### 3.1 Obliczanie różnicy czasowej

delta_ramek = numer_obecnej_klatki - numer_poprzedniej_klatki

#### 3.2 Tworzenie macierzy kosztów
Dla każdej pary (obiekt_obecny, obiekt_poprzedni) oblicza:

**Odległość przestrzenną:**
- Znajduje środki obiektów:  (x + width/2, y + height/2) 
- Oblicza odległość euklidesową między środkami
- Normalizuje przez różnicę klatek:  odległość / delta_ramek 

**Podobieństwo obszarów:**
- Oblicza powierzchnie:  width * height 
- Wyznacza współczynnik:  min(area1, area2) / max(area1, area2) 

**Predykcja ruchu (jeśli dostępna historia):**
- Bierze 2 ostatnie pozycje z historii
- Oblicza prędkość:  (pos2 - pos1) / delta_ramek_historii 
- Przewiduje pozycję:  ostatnia_pozycja + prędkość * delta_ramek 
- Oblicza odległość od przewidywanej pozycji

**Końcowy koszt:**

koszt = 0.6 * (odległość_znormalizowana / próg_dystansu) + 0.4 * (1 - podobieństwo_obszaru) - 0.25 * bonus_za_predykcję


#### 3.3 Filtrowanie możliwych przypisań
- Odrzuca pary gdzie odległość > próg_dystansu (50 pikseli)
- Odrzuca pary gdzie podobieństwo < min_podobieństwo (0.3)

#### 3.4 Algorytm węgierski - łączenie z prawdopodobieństwem
- Używa  scipy.optimize.linear_sum_assignment 
- Znajduje optymalne przypisanie minimalizujące całkowity koszt
- Odrzuca przypisania o koszcie > 0.75

#### 3.5 Aktualizacja historii ruchu
- Dla każdego przypisanego obiektu dodaje nową pozycję do historii
- Ogranicza historię do ostatnich 4 pozycji
- Historia przechowuje środki obiektów: [center_x, center_y, width, height]

### 4. Zapis wyników

## Parametry algorytmu

- **prog_dystansu**: 50 pikseli - maksymalna odległość dla przypisania
- **min_podobienstwo**: 0.3 - minimalny próg podobieństwa obszarów
- **próg_akceptacji**: 0.75 - maksymalny koszt dla zaakceptowania przypisania
- **rozmiar_historii**: 4 pozycje - ile ostatnich pozycji pamiętać

## Wyniki

System generuje:

- **Konsola**: Wyniki śledzenia w czasie rzeczywistym
- **tracking_results.txt**: Pełne wyniki śledzenia
- **Metryki dokładności**: Przy dostępności danych referencyjnych

## Zastosowania

System jest szczególnie przydatny w:

- Automatyce przemysłowej
- Monitoringu wizyjnym
- Analizie ruchu obiektów
- Systemach bezpieczeństwa
- Badaniach naukowych

## Struktura projektu

├── main.py # Główny plik aplikacji

├── README.md # Dokumentacja

└── frames/ # Folder z baza klatek

├── bboxes.txt # Dane wejściowe

├── bboxes_gt.txt # Dane referencyjne (opcjonalne)

└── tracking_results.txt # Wyniki


## Licencja

MIT License

## Autor
## Jakub Lesniarek
## Piotr Skoracki
