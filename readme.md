**Python kursa noslēguma projekts**
**“HexiPuzzle”**

**Grupas dalībnieki**
Kārlis Mārtiņš Zīverts kz22059
Edgars Tamisārs et22022

**Apraksts**
HexiPuzzle ir spēle, kuras mērķis ir, pārvietojot, rotējot un apvēršot dotos gabaliņus, pilnībā aizpildīt izvēlēto režģi. Neviena gabaliņa daļa nedrīkst pārklāties ar citiem, vai iziet ārpus režģa robežām.

Puzles gabaliņi ir figūras, kuras sauc par heksamondiem. Tie katrs sastāv no 6 vienādmalu trijstūriem. Eksistē 12 dažādu formu heksamondi. 
Spēlētājam vienmēr ir pieejams tieši viens no katras formas un tie vienmēr tiek parādīti formai raksturīgajā krāsā.
Spēlētājs var izmantot dažus vai visus 12 heksamondus, lai aizpildītu režģi.

Ir pieejamas 3 grūtības pakāpes: easy, medium, hard. Pēc grūtības izvēles, spēlētājs izvēlas režģi, kuru vēlas salikt.

Spēlētāja progress katrā režģī saglabājas programmas darbības laikā, kā arī starp palaišanas reizēm.

**Instrukcija**
Lai sāktu programmu, palaidiet skriptu HexiPuzzle.py


Gabaliņu pārvietošana - kreisais peles klikšķis
Gabaliņu rotēšana - labais peles klikšķis
Gabaliņu horizontāla apvēršana - “spacebar”

Pārvietojot gabaliņu, baltas apmales norāda, ka atlaižot gabaliņu šajā vietā, tas veiksmīgi tuvākajā pozīcijā piestiprināsies režģim. 

Spēles skata opcija “Clean up” atiestata pozīcijas tiem gabaliņiem, kuri šobrīd nav piestiprināti režģim.
Spēles skata opcija “Reset progress” atiestata pozīcijas visiem gabaliņiem šajā režģī.
Sākuma skata opcija “Reset all progress” atiestata gabaliņu pozīcijas visos režģos.


**Projekta GitHub repozitorijs**
https://github.com/Karlukki/HexiPuzzle


Trijstūru režģa koordinātu sistēmas implementācijai (transformācijas, pārveidošana uz dekarta koordinātu sistēmu), tika izmantots updown_tri.py modulis no publiska Github repozitorija https://github.com/BorisTheBrave/grids
