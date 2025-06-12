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

System oczekuje pliku `bboxes.txt` w następującym formacie:
c6s1_000451.jpg

1

420.836933 144.188985 88.328294 216.466523

c6s1_000476.jpg

3

325.044276 151.653348 126.894168 204.025918

177.001080 160.361771 90.816415 153.019438

129.726782 129.260259 83.352052 195.317495

Gdzie:
- Pierwsza linia: nazwa pliku obrazu
- Druga linia: liczba obiektów w klatce
- Następne linie: współrzędne obiektów w formacie x,y,width,height
## Użycie

### Podstawowe śledzenie

python main.py /path/to/data/folder


### Śledzenie z ewaluacją

Jeśli folder zawiera plik `bboxes_gt.txt` z danymi referencyjnymi:


System automatycznie wykryje dane referencyjne i wyświetli dokładność śledzenia.

## Parametry konfiguracyjne

- prog_dystansu: Maksymalny dystans dla przypisania obiektów (domyślnie: 50)
- min_podobienstwo: Minimalny próg podobieństwa obszarów (domyślnie: 0.3)

## Algorytm

System wykorzystuje następujące komponenty:

1. **Macierz kosztów** - Obliczanie kosztów przypisania na podstawie:
   - Dystansu między obiektami
   - Podobieństwa obszarów
   - Predykcji ruchu

2. **Algorytm węgierski** - Optymalne rozwiązanie problemu przypisania

3. **Historia ruchu** - Śledzenie pozycji obiektów dla lepszej predykcji

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
