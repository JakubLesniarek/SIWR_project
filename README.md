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

frame_001.jpg
2
x1 y1 width1 height1
x2 y2 width2 height2
frame_002.jpg
2
x1 y1 width1 height1
x2 y2 width2 height2

## Użycie

### Podstawowe śledzenie

python main.py /path/to/data/folder


### Śledzenie z ewaluacją

Jeśli folder zawiera plik `bboxes_gt.txt` z danymi referencyjnymi:


System automatycznie wykryje dane referencyjne i wyświetli dokładność śledzenia.

## Format danych referencyjnych

Plik `bboxes_gt.txt` powinien zawierać:

frame_001.jpg
2
id1 x1 y1 width1 height1
id2 x2 y2 width2 height2


## Parametry konfiguracyjne

- `prog_dystansu`: Maksymalny dystans dla przypisania obiektów (domyślnie: 50)
- `min_podobienstwo`: Minimalny próg podobieństwa obszarów (domyślnie: 0.3)

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
Jakub Lesniarek
Piotr Skoracki
