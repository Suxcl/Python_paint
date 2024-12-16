'''
Projekt 4
Wymagania na najwyższą ocenę:

a. Przekształcenia punktowe

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i wykonywanie na nim poniższych operacji:
Dodawanie (dowolnych podanych przez użytkownika wartości),
Odejmowanie (dowolnych podanych przez użytkownika wartości),
Mnożenie (przez dowolne podane przez użytkownika wartości),
Dzielenie (przez dowolne podane przez użytkownika wartości),
Zmiana jasności (o dowolny podany przez użytkownika poziom),
Przejście do skali szarości (na dwa sposoby)


b. Metody polepszania jakości obrazów

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i aplikowanie do niego poniższych filtrów:
Filtr wygładzający (uśredniający),
Filtr medianowy,
Filtr wykrywania krawędzi (sobel),
Filtr górnoprzepustowy wyostrzający,
Filtr rozmycie gaussowskie,
Splot maski dowolnego rozmiaru i dowolnych wartości elementów maski (opcjonalne za dodatkowe punkty)
Filtr wygładzający:
⎡⎣⎢111111111⎤⎦⎥

Filtr wykrywania krawędzi (pionowy i poziomy):
⎡⎣⎢−1−2−1000121⎤⎦⎥
⎡⎣⎢10−120−210−1⎤⎦⎥

Filtr górnoprzepustowy wyostrzający:
⎡⎣⎢−1−1−1−19−1−1−1−1⎤⎦⎥

Filtr Gaussa:
⎡⎣⎢121242121⎤⎦⎥


Uwagi:
Zabronione stosowanie bibliotek do implementacji przekształceń punktowych i filtrów


------------------------------------------------------------------------

Projekt 5 
Histogram - wyrównanieAdres URL
http://www.algorytm.org/przetwarzanie-obrazow/histogram-wyrownywanie.html
Histogram - rozciąganie
http://www.algorytm.org/przetwarzanie-obrazow/histogram-rozciaganie.html
Metody automatycznego dobierania progu binaryzacji
https://www.olympus-lifescience.com/en/microscope-resource/primer/java/digitalimaging/processing/automaticthresholding/

Wymagania na najwyższą ocenę:

a. Histogram

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i zaprezentowanie działania normalizacji obrazu poprzez:
Rozszerzenie histogramu,
Wyrównanie (equalization) histogramu.
b. Binaryzacja

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2) i zaprezentowanie działania binaryzacji z ustaleniem progów binaryzacji w następujący sposób:
Ręcznie przez użytkownika - użytkownik podaje próg bezpośrednio,
Procentowa selekcja czarnego (ang. Percent Black Selection),
Selekcja iteratywna średniej (ang. Mean Iterative Selection),
Selekcja entropii (ang. Entropy Selection),
Błąd Minimalny (ang. Minimum Error),
Metoda rozmytego błędu minimalnego (ang. Fuzzy Minimum Error).
Uwagi:
Spośród powyższych sposobów binaryzacji konieczna jest implementacja sposobu 1 oraz dwóch wybranych spośród 2 - 6. Za implementację więcej niż dwóch sposobów binaryzacji wybranych spośród 2 - 6 przyznane zostaną dodatkowe punkty.
Zabronione jest stosowanie bibliotek w implementacji normalizacji i binaryzacji.

------------------------------------------------------------------------

Projekt 6
Wymagania na najwyższą ocenę:

Rysowanie krzywej Béziera,
Program może rysować krzywą Béziera o dowolnym stopniu; stopień rysowanej krzywej powinien zostać podany przez użytkownika,
Punkty charakterystyczne krzywej Béziera można podać podczas tworzenia za pomocą myszy lub przy pomocy pól tekstowych,
Punkty charakterystyczne krzywej Béziera można modyfikować za pomocą myszy (chwytanie i przeciąganie) oraz przy pomocy pól tekstowych,
Przy modyfikacji krzywej Béziera przy pomocy myszy zmiany na ekranie można obserwować na bieżąco - krzywa jest przeliczana w czasie rzeczywistym i zmiany są na bieżąco rysowane.
Bj=∑ni=0(ni)(1−jk−1)n−i(jk−1)iPi

n - stopień krzywej = liczba punktów charakterystycznych - 1
k - liczba punktów krzywej
Bj - j-ty punkt krzywej, 0 ≤ j ≤ k - 1
Pi - i-ty punkt charakterystyczny, 0 ≤ i ≤ n

Uwagi:
Zabronione stosowanie bibliotek do rysowania krzywych.

------------------------------------------------------------------------

Projekt 7
Przekształcenia 2D
https://eduinf.waw.pl/inf/utils/002_roz/2008_21.php

Wymagania na najwyższą ocenę:

Definiowanie i rysowanie dowolnych figur - wielokątów przy użyciu myszy lub pól tekstowych,
Wykonywanie następujących przekształceń na stworzonych figurach:
Przesunięcie o zadany wektor,
Obrót względem zadanego punktu o zadany kąt,
Skalowanie względem zadanego punktu o zadany współczynnik,
Figury powinny być chwytane przy użyciu myszy
Wszystkie operacje powinny móc być wykonywane zarówno przy pomocy myszy, jak i za pomocą pól tekstowych:
Przesunięcie - przy użyciu myszy oraz po podaniu wektora i zatwierdzeniu,
Obrót - definiowanie punktu obrotu przy użyciu myszy oraz za pomocą pól tekstowych, wykonywanie obrotu przy użyciu myszy (chywanie i obracanie) oraz poprzez podanie i zatwierdzenie kąta obrotu w polu tekstowym,
Skalowanie - definiowanie punktu skalowania przy użyciu myszy oraz za pomocą pól tekstowych, wykonywanie skalowania przy użyciu myszy (chwytanie i skalowanie) oraz poprzez podanie i zatwierdzenie współczynnika skalowania w polu tekstowym,
Możliwość serializacji i deserializacji (zapisywanie i wczytywanie), tak aby za każdym uruchomieniem programu nie było konieczności rysowania figur od nowa.
Uwagi: 
Zadanie wykonujemy zakładając transformacje przy użyciu współrzędnych jednorodnych
Zabronione stosowanie bibliotek w implementacji przekształceń

------------------------------------------------------------------------

JAK RESZTA WYJDZIE GIT TO NIE TRZEBA 8


Projekt 8 


Operacje morfologiczneAdres URL
https://hackmd.io/@8dSak6oVTweMeAe9fXWCPA/SkiN5TuVO

Wymagania na najwyższą ocenę:   

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2),
Implementacja następujących filtrów morfologicznych oraz zaprezentowanie ich działania na wczytanym obrazie:
Dylatacja,
Erozja,
Otwarcie,
Domknięcie,
Hit-or-miss (pocienianie i pogrubianie)
Uwagi:
Użytkownik powinien mieć możliwość własnego zdefiniowania elementu strukturyzującego dowolnego rozmiaru
Zabronione stosowanie bibliotek w implementacji filtrów

------------------------------------------------------------------------

Projekt 9 - jesli add

Wymagania na najwyższą ocenę:

Wczytanie obrazu (np. w analogiczny sam sposób, jaki był wykonany w ramach Projektu 2),
Obliczenie, ile procent wczytanego obrazu stanowią tereny zielone,
Wykonywanie obliczeń powinno odbywać się w sposób wydajny,
Wyniki obliczeń powinny być możliwie dokładne,
Wykorzystana metoda obliczeń jest w pełni dowolna; Należy wykorzystać materiały i podpowiedzi z wykładu;
Uwagi:
Mile widziana możliwość parametryzacji programu, tak aby nie brał pod uwagę wyłącznie terenów zielonych, a także inne kolory / warunki wejściowe.

------------------------------------------------------------------------

'''