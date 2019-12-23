# Generování a procházení bludiště

Tento program v jazyce Python generuje bludiště, která následně umožní uživateli kompetitivní formou projít.

Program se skládá ze dvou částí: Pomocí první části se pouze vygeneruje několik základních bludišť (levelů), které jsou uložené v souboru. S touto částí programu nebude uživatel nijak interagovat. 

Druhá část programu je hra samotná, která umožní zahájit procházení předem vytvořených levelů na čas. Zároveň si v hlavním programu může uživatel projít náhodně generované bludiště, které se již nikam neukládá. Tato část programu je interaktivní.

S programem bude uživatel komunikovat pomocí klávesnice. Jedná se především o pohyb v rámci menu a poté pohyb bludištěm. 

Na hru jako takovou bude použita knihovna pygame.

Vygenerovaná bludiště se ukládají, tak jako nejlepší skóre hráče, do souboru, ze kterého jsou také načítány.


