# Generování a procházení bludiště

Tento program v jazyce Python generuje bludiště, která následně umožní uživateli kompetitivní formou projít.

Program se skládá ze dvou částí: Pomocí první části se pouze vygeneruje několik základních bludišť (levelů), které jsou uložené v souboru. S touto částí programu nebude uživatel nijak interagovat. 

Druhá část programu je hra samotná, která umožní zahájit procházení předem vytvořených levelů na čas. Zároveň si v hlavním programu může uživatel projít náhodně generované bludiště, které se již nikam neukládá. Tato část programu je interaktivní.

S programem uživatel komunikuje pomocí klávesnice. Jedná se především o pohyb v rámci menu a poté pohyb bludištěm. 

Na hru jako takovou je použita knihovna pygame.

Vygenerovaná bludiště se ukládají, tak jako nejlepší skóre hráče, do souboru, ze kterého jsou také načítány.

## Použití

Pro spuštění s defaultními parametry spusťte [main.py](Zapoctovy_program/main.py).


Příklad použití v kódu 🐍:

```python
from zapoctak import napis_zapoctak

muj_zapoctak = napis_zapoctak(jazyk='python', zajimavost=17)
print(muj_zapoctak[::-1].upper())

muj_zapoctak = napis_zapoctak(jazyk='🐍', zajimavost=3)
print(muj_zapoctak)
```

Výsledek:

```
NPOYYPYYPYHHPNOOO🐍
🐍🐍🐍
```

Je hezké mít hned na začátku různé příklady vstupů a výstupů, obrázky, a podobně.

Inspirujte se u jiných knihoven, například:
- [tqdm](https://github.com/tqdm/tqdm) (progress bar, doporučuji využívat :)),
- [transformers](https://github.com/huggingface/transformers) (jazyková záležitost).

## Instalace a požadavky
Pro spuštění [main.py](Zapoctovy_program/main.py) je potřeba mít nainstalovanou knihovnu Pygame verze 1.9.6, pro spuštění [Level_generator.py](Zapoctovy_program/Level_generator.py) není třeba žádná další knihovna.

## Dokumentace

Podstatná část dokumentace je tvořena dobře čitelným, místy okomentovaným kódem.
