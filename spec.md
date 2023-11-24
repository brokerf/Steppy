# Steppy, a stepper for Python

## Statements and expressions

Features

* variables, assignment, expressions
* print

Eingabe(datei):

```python
celsius = 36
fahrenheit = (celsius * 9/5) + 32
print(fahrenheit)
```

Die Ausgabe ist immer ein `Block`, bestehend aus drei Teilen jeweils getrennt durch einen Strich `######`.

1. Die Variablen mit ihren aktuellen Werten.
2. Ausgaben
3. Die Statements, die noch ausgeführt werden müssen.

Dieses Format hat die Eigenschaft, dass jeder Zwischenschritt wieder ein gültiges Python-Skript ist, ausgeführt werden kann und dasselbe Ergebnis/Ausgaben liefert wie das ursprüngliche Skript.

Startzustand (1. Ausgabe)

```python
###################
###################
celsius = 36
fahrenheit = (celsius * 9/5) + 32
print(fahrenheit)
```

Erster Schritt: `36` ist ausgewertet, also Ausführung der Zuweisung:

```python
celsius = 36 
###################
###################
fahrenheit = (celsius * 9/5) + 32
print(fahrenheit)
```

Jetzt: schrittweise Auswertung von `(celsius * 9/5) + 32`.
Die Teilausdrücke werden von links nach rechts bearbeitet.
Nachschlagen des Werts von `celsius`:

```python
celsius = 36 
###################
###################
fahrenheit = (36 * 9/5) + 32
print(fahrenheit)
```

Nächster Teilausdruck `9/5` --> `1.8`

```python
celsius = 36 
###################
###################
fahrenheit = (36 * 1.8) + 32
print(fahrenheit)
```

Nächster Teilausdruck `36 * 1.8` --> `64.8`

```python
celsius = 36 
###################
###################
fahrenheit = 64.8 + 32
print(fahrenheit)
```

Nächster Teilausdruck `64.8 + 32` --> `96.8`

```python
celsius = 36 
###################
###################
fahrenheit = 96.8
print(fahrenheit)
```

Zuweisung

```python
celsius = 36 
fahrenheit = 96.8
###################
###################
print(fahrenheit)
```

Variable `fahrenheit` nachschlagen

```python
celsius = 36 
fahrenheit = 96.8
###################
###################
print(96.8)
```

Ausgabe `96.8`

```python
celsius = 36 
fahrenheit = 96.8
###################
print(96.8)
###################
```

Fertig!

## Konditional

```python
x = 3
if x>0:
    y = 1
else:
    y = 42
```

Start; nach der ersten Zuweisung

```python
x = 3
####################
####################
if x>0:
    y = 1
else:
    y = 42
```

Variable `x`

```python
x = 3
####################
####################
if 3>0:
    y = 1
else:
    y = 42
```

Ausdruck `x>0`

```python
x = 3
####################
####################
if True:
    y = 1
else:
    y = 42
```

If-True: if-Block wird ausgeführt, else-Block fällt weg

```python
x = 3
####################
####################
y = 1
```

Zuweisung

```python
x = 3
y = 1
####################
####################
```

Fertig.

