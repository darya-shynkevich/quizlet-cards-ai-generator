from generator.config import Config

DEFAULT_DICTIONARY_URLS = [
    "wsjp.pl",
]


def get_target_dictionary_urls() -> str:
    dictionary_urls = Config.DICTIONARY_URLS or DEFAULT_DICTIONARY_URLS
    return "|".join(dictionary_urls)


prompt_preamble = f"""Chcę, żebyś zachowywał się jak profesjonalny twórca kart Anki, potrafiący tworzyć karty Anki na podstawie dostarczonego przeze mnie tekstu.

Formułując treść karty należy kierować się dwiema zasadami.
1. Minimalne informacje: Materiał do nauki powinien być prosty, ale kompleksowy i nie pomijać skomplikowanych szczegółów.
2. Zoptymalizowane sformułowanie: Upewnij się, że sformułowanie karty umożliwia szybkie zrozumienie i reakcję, co ma na celu zmniejszenie liczby błędów i zwiększenie koncentracji.
3. Użyj {get_target_dictionary_urls()} jako głównego źródła definicji i przykładów

Obsługa kontekstu:
- Podaj karty z kontekstem lub bez:
 - Brak kontekstu: Jeśli nie podano kontekstu, użyj lub utwórz odpowiedni kontekst.
 - Z kontekstem: Użyj podanego kontekstu. Jeżeli kontekst zniekształca konwencjonalne użycie słowa, należy go zignorować.
- Nie mieszaj pól kontekstu na karcie i upewnij się, że kontekst ma znaczenie dla zawartości karty.

Format wejściowy:
- Potrafię podać słowo lub frazę bez kontekstu:
 - SŁOWO: [słowo docelowe]; KONTEKST: []
- Alternatywnie mogę podać słowo lub frazę z kontekstem:
 - SŁOWO: [słowo docelowe]; KONTEKST: [kontekst]

Oczekiwania wyjściowe:
- Wyklucz niepowiązane zdania, jako „Przykład karty”.
- Nie można użyć słowa z wejścia na wyjściu. Wszystkie litery należy maskować podkreśleniami.
- Wynik powinien zawierać wyłącznie tekst karty.
- Powinieneś dodać 4-5 zdań skupiających się wyłącznie na wyjaśnieniu zamaskowanego słowa lub wyrażenia.
- Pomiędzy definicją a przykładami powinien znajdować się pusty symbol \n

Zasady maskowania:
- Zamaskuj słowo docelowe znakami podkreślenia, zachowując spacje między słowami („wolna wola” zmieni się na „____ ____”).
- Liczba podkreśleń powinna odpowiadać liczbie liter („zbawienie” zmieni się na „_________”)
- Maskuj tylko słowo docelowe, a nie jego kontekstowe użycie. Na przykład „zajęcie” w wyrażeniu „zajęcie statku” powinno jedynie maskować „zajęcie”.
- Jeśli słowo zawiera cząstkę się, to cząstkę zmieni na ___
"""


def examples() -> str:
    examples_preamble = """
    Oto kilka przykładów w formacie
    SŁOWO: [słowo docelowe]; KONTEKST: [kontekst opcjonalny]; WYNIK: [co spodziewam się uzyskać jako wynik]
    """

    _examples = {
        "działać": [
            "",
            "Wpływać na kogoś lub coś, w ten sposób, że wchodzi w określony stan"
            "Przykłady:"
            "1. benzen, kwas (askorbinowy, mrówkowy...); lekarstwo, tabletka; alkohol, kawa; klimat, powietrze; jakaś sytuacja _____a na kogoś/coś"
            "2. _____ na organizm, na układ nerwowy; na emocje, na uczucia, na wyobraźnię"
            "3. pozytywnie _____; _____ destrukcyjnie, negatywnie, toksycznie, usypiająco"
            "4. _____ jak narkotyk",
        ],
        "drażnić": [
            "",
            "Wywoływać w kimś negatywne emocje, zwykle niezadowolenie lub złość. "
            """"
            Przykłady:
            1. ______i czyjaś obecność, czyjś wygląd, czyjeś zachowanie, widok czegoś; bezczynność, bezruch, niesprawiedliwość; odgłos, stukot, szelest; ______ią reklamy
            2. ______ męża, społeczeństwo, wyborców
            3. ______ bogactwem; wyglądem; zachowaniem, bezmyślnością, naiwnością, poglądami
            4. ______ najbardziej, niebywale, niewymownie, szczególnie
            5. zaczynać ______
            6. ______ i niepokoić, ______ i denerwować,______ i niecierpliwić, ______ i przeszkadzać, ______ i prowokować, ______ i dekoncentrować
            """,
        ],
        "gapić się": [
            "",
            "Patrzeć na kogoś lub na coś bezmyślnie przez dłuższy czas."
            """
            Przykłady:
            1. motłoch, tłum ____ ___; faceci, turyści _____ ___
            2. _____ ___ na coś całymi dniami, godzinami; szeroko otwartymi oczami
            3. _____ ___ na chmury, na ekran, na kobiety, na słońce, na ścianę, na wystawy, na zdjęcia
            4. _____ ___ przez okno
            5. _____ ___ w ekran, w gwiazdy, w komputer, w lustro, w monitor, w okno, w sufit, w szpary, w ścianę, w telewizor, w ziemię
            6. _____ ___ na coś z nudów; z bliska; z niedowierzaniem
            7. _____ ___ bezmyślnie, długo, ponuro, tępo lubić, przestać, zacząć _____ ___
            8. leżeć i _____ ___, siedzieć i _____ ___
            """,
        ],
    }

    anki_examples_strings = [
        f"SŁOWO: [{word}]; KONTEKST: [{_examples[word][0]}]; WYNIK:[{_examples[word][1]}]\n"
        for word in _examples.keys()
    ]
    return examples_preamble + "".join(anki_examples_strings)


def rule_language_level() -> str:
    return f"""
    Language Level:
    - A person with the language level [{Config.LEVEL}] should understand the card.
    - Words and constructions that should be familiar to a person at this level.
    - If the language level is set to C1 or C2, use words and constructions of your choice.
    """


def get_prompt() -> str:
    return prompt_preamble + rule_language_level() + examples()
