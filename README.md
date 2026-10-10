# Cykeluthyrning – testing och refactoring

## Mål

Öva att låta ett test beskriva en regel, se det bli **RED**, ändra implementationen och se det bli **GREEN**. Du tränar också på att tester fångar regressioner: gamla gröna tester ska fortsätta vara gröna när koden ändras. Labben tar ungefär **90–120 minuter**. Den är liten med avsikt: fem functions och ett bike-`dict`, utan classes eller ny arkitektur.

## Kom igång

Från mappen med denna README, installera en gång och kör sedan testerna:

```text
python -m pip install -r requirements.txt
python -m pytest
```

Om `python` inte hittas, prova `py` på Windows eller `python3` på vissa datorer. Använd samma Python-kommando vid installation och körning. Du arbetar i [test_bike_rental.py](test_bike_rental.py) och [bike_rental.py](bike_rental.py). Testfilen har **exakt ett** färdigt exempeltest. Det ska passera från start. Skriv dina egna tester nedanför det.

En cykel ser ut så här: `{"id": 101, "is_available": True}`. Skapa ett **nytt** bike-`dict` i varje test som behöver en cykel, så att testernas `state` inte påverkar varandra. Vi använder heltal för `hours` och `hourly_rate`; inmatning och exception handling ingår inte. Ett nekat anrop ska returnera `False` och lämna cykelns `state` oförändrat. `calculate_price()` ska ge `None` för ogiltig hyrestid.

## Arbetsmodell

```text
RED
Skriv ett test för ett beteende som ännu inte uppfylls.

GREEN
Ändra implementationen tills testet passerar.

REFACTOR
Förbättra kodens struktur utan att avsiktligt ändra beteendet.
Kör sedan alla tester igen.
```

Om ett tidigare grönt test blir rött efter refactoring har något befintligt beteende förändrats. Det är en **regression** (ett **regressionsfel**). Ett rött test i den här labben är också väntat efter att du skrivit en ny förväntning. Läs vilket `assert` som failade innan du ändrar koden. Skriv ett test i taget. Om du fastnar: kontrollera testets data, förväntat värde och vilken function som faktiskt anropas. Git är sekundärt; en liten `commit` efter några gröna steg räcker.

## Steg 1 – se en grön baseline

**Mål:** Veta att projektet fungerar innan du ändrar det. **Gör:** Kör `python -m pytest` och läs det enda testet: vad är Arrange, Act och Assert? **Klar när:** Du ser `1 passed` och kan förklara varför två timmar à 50 ger 100. Ändra ingen kod än.

## Steg 2 – hyrestid större än noll

**Mål:** En hyrestid på `0` eller `-1` ska ge `False`, medan `2` ska ge `True`. **Gör:** Skriv först ett test för `is_valid_rental_hours(0)` med förväntat `False`. Kör pytest: det ska bli **RED**. Ändra sedan bara `is_valid_rental_hours()` tills testet är **GREEN**. Lägg till ett test för `-1` och ett för `2`; kör igen. **Klar när:** Alla tre svaren är rätt och starttestet fortfarande passerar.

## Steg 3 – gränsen 24 timmar

**Mål:** `24` är giltigt men `25` är ogiltigt. **Gör:** Skriv test för båda. Kör **före** kodändringen: `25` ska bli **RED**. Utöka samma lilla regel i `is_valid_rental_hours()` och kör igen. **Klar när:** `24` ger `True`, `25` ger `False`, och testerna från steg 1–2 är fortsatt gröna.

## Steg 4 – bara en ledig cykel får hyras

**Mål:** `can_rent_bike()` ska svara `True` för en ledig cykel och `False` för en redan uthyrd. **Gör:** Skriv två tester med varsitt nytt bike-`dict`; sätt `is_available` till `False` i det andra. Kör: det nekade fallet ska bli **RED**. Ändra `can_rent_bike()` så att den läser cykelns `state` utan att ändra det. **Klar när:** Båda testerna är gröna och dictionaries är oförändrade efter validation-anropet.

## Steg 5 – lyckad uthyrning

**Mål:** Ett lyckat `rent_bike(bike, 2)` ska returnera `True` och ändra `is_available` från `True` till `False`. **Gör:** Skriv ett test som kontrollerar **både** return-värdet och cykelns `state`. Kör pytest. Det här happy-path-testet kan vara **GREEN direkt**; behåll det som skydd mot en regression i steg 7. **Klar när:** Testet är grönt och du kan visa de två separata `assert`-kontrollerna.

## Steg 6 – nekad uthyrning ska inte ändra state

**Mål:** Ogiltig tid eller redan uthyrd cykel ska ge `False` utan state-ändring. **Gör:** Börja med en **ledig** cykel och `hours = 0`. Skriv ett test för return-värde **och** att `is_available` fortfarande är `True`. Kör: minst en förväntning ska bli **RED**. Ändra `rent_bike()` så att den använder dina validation functions **före** tilldelningen. Kör igen. Lägg till egna tester för negativ tid, `25` timmar och en redan uthyrd cykel. **Klar när:** Dina tester skyddar giltig tid, `0`, negativ tid, `24`, `25`, ledig och uthyrd cykel, lyckad uthyrning och state-ändring samt nekad uthyrning utan state-ändring. Kör `python -m pytest`: alla tester ska nu vara **GREEN**.

## Steg 7 – när en refactoring skapar en regression

**Mål:** Se hur gamla tester skyddar fungerande beteende. Refactoring betyder att ändra kodens struktur utan att avsiktligt ändra dess beteende. **Gör:** Kör `python -m pytest` och verifiera att alla tester du hittills skrivit är **GREEN**. Ändra inget förrän dessförinnan: de ska nu fungera som vårt säkerhetsnät.

Vi provar att skriva om `rent_bike()` till en kortare variant. Den ser vid första anblicken rimlig ut. Ändra **inte testerna**:

```python
def rent_bike(bike, hours):
    if is_valid_rental_hours(hours) and can_rent_bike(bike):
        bike["is_available"] = False

    return True
```

Kör `python -m pytest` igen. Läs failures: vilka testnamn failar? Vilket `assert` failar? Vad förväntade testet, vad returnerar implementationen nu och ändrades `state`? Varför passerar happy-path-testet fortfarande? Ett enda grönt happy-path-test hade inte avslöjat felet; de andra testerna skyddade beteenden som redan fungerade.

Ändra **implementationen – inte testerna**. Återställ korrekt beteende: giltig uthyrning ger `True`; ogiltig tid och redan uthyrd cykel ger `False`; `state` ändras bara vid tillåten uthyrning. Hint: Fundera på vad `rent_bike()` ska returnera när `if`-villkoret är `False`. Kör testerna igen: alla tidigare tester ska vara **GREEN**.

> **Tester skyddar gammalt beteende när koden förändras.** Ett test är inte bara till för att kontrollera ny kod. Det kan också upptäcka när något som fungerade tidigare går sönder. Det är ett **regressionsfel**.

**Klar när:** Du har sett nekade uthyrningstester bli röda, fixat implementationen utan att ändra testerna och fått hela testsamlingen grön igen. ändra tillbaka till fungerande kod innan du fortsätter.

## Steg 8 – returnera en cykel

**Mål:** En uthyrd cykel kan returneras; en redan ledig cykel kan inte returneras igen. **Gör:** Skriv ett test där `is_available` börjar som `False`: `return_bike()` ska ge `True` och ändra värdet till `True`. Skriv sedan ett test för en redan ledig cykel: förvänta `False` och oförändrat `True`. Kör **innan** ändring: det senare testet ska bli **RED**. Lägg en enkel kontroll före state-ändringen i `return_bike()` och kör igen. **Klar när:** Båda fallens return-värde och `state` är rätt.

## Steg 9 – pris och hel körning

**Mål:** Pris är `hours * hourly_rate` bara för giltig tid. **Gör:** Starttestet täcker redan `2 * 50 = 100`. Skriv ett test där `hours = 0` och förväntat resultat är `None`. Kör: det ska bli **RED**. Ändra `calculate_price()` så att den återanvänder `is_valid_rental_hours()` och ger `None` för ogiltig tid. Prova gärna också `25` timmar. Kör `python -m pytest` en sista gång. **Klar när:** Alla tester är gröna och din testfil täcker giltig/ogiltig tid, `24`/`25`, ledig/uthyrd cykel, lyckad/nekad uthyrning, returnering och pris. Om tiden tar slut: prioritera steg 1–8 och återkom hit senare.

## När du är klar

Fundera kort: Vad var skillnaden mellan validering och testing? Varför skrev du testet **före** ändringen? Vad betyder RED? Varför kontrollerade du `state` efter en nekad operation? Hur fångade testerna en regression? Vad ger gröna tester dig nästa gång koden ändras?

Facit finns i `facit/`. Försök göra hela **RED → GREEN**-cykeln själv innan du jämför. Ett möjligt tillfälle för en liten `commit` är efter steg 3 (`Add rental validation tests`), steg 6 (`Fix rejected rental state`) eller steg 7 (`Demonstrate rental regression`).
