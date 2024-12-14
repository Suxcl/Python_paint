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
'''