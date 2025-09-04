co ma na celu program - program ma na celu analize rynku gpw ściąganie aktualnych cen codziennie po zamknieciu niech pobiera wszystkie spółki z giełdy oraz nowości z internetu newsow itp tak aby wyszukiwac najlepsze spolki pod inwestycje na rozne terminy itp. badz szybki zysk i docelowo ma wyszukiwac takich spolek ktore posiadaja:

Regularny wzrost przychodów
Regularny wzrost zysku operacyjnego
Działa na rosnącym rynku
Zarząd wywiązuje się ze składanych deklaracji
Szacujemy, że rozwój będzie kontynuowany
Idealnie byłoby gdybyśmy mieli podstawy sądzić, że rozwój z jakichś powodów przyspieszy

### **Kluczowe funkcjonalności**

1. **Zbieranie danych rynkowych (Data Collection)**
    - Automatyczne pobieranie cen akcji wszystkich spółek z scrapingu (data_collector.py)
    - Zbieranie i archiwizacja danych historycznych (kursy, wolumen, kapitalizacja).
    - Pobieranie raportów finansowych spółek (przychody, zyski, wskaźniki).
2. **Analiza fundamentalna spółek**
    
    Program automatycznie ocenia:
    
    - **Regularny wzrost przychodów** (Revenue Growth).
    - **Regularny wzrost zysku operacyjnego** (EBIT, Net Profit).
    - Branżę i **wielkość rynku, na którym działa spółka**.
    - Skuteczność zarządu na podstawie wcześniejszych zapowiedzi i wyników.
    - Prognozę dalszego rozwoju na podstawie trendów finansowych i rynkowych.
    - Szacowanie potencjalnego przyspieszenia wzrostu (trigger news, nowe produkty, zmiany w branży).
3. **Analiza techniczna** (opcjonalny moduł)
    - Automatyczne generowanie sygnałów technicznych (SMA, EMA, RSI, MACD).
    - Wykresy i wizualizacje trendów cenowych.
4. **Analiza sentymentu (NLP, AI)**
    - Automatyczne pobieranie newsów, komunikatów ESPI/EBI, artykułów branżowych.
    - Analiza treści pod kątem **sentymentu (pozytywny/negatywny/neutralny)** i wykrywanie triggerów (np. akwizycje, nowe kontrakty).
    - System rankingowy przypisujący spółkom „punktację sentymentu”.
5. **Dashboard i interfejs użytkownika (Streamlit)**
    - Przejrzysty panel, gdzie inwestor widzi:
        - Aktualne kursy i ich zmiany.
        - Ranking najlepszych spółek wg kryteriów fundamentalnych i sentymentu.
        - Wykresy trendów, raporty kwartalne, alerty.
        - Automatyczne powiadomienia o zmianach na rynku.
6. **Baza danych i archiwizacja**
    - Dane przechowywane w bazie SQL/NoSQL (np. PostgreSQL, MongoDB).
    - Możliwość analizy danych historycznych oraz backtestów strategii inwestycyjnych.
