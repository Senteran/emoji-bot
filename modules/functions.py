def to_en_str(pl_str):
    # Przechowuje polskie znaki oraz ich odpowiedniki aby móc je zamienić (Nie jestem pewny co do 'ó' może by to zmienić na 'o' zamiast?)
    polish_symbols = {
        'ą': 'a',
        'ć': 'c',
        'ę': 'e',
        'ó': 'o',
        'ż': 'z',
        'ź': 'z',
        'ł': 'l',
        'ś': 's',
        'ń': 'n'
    }
    
    # Stworzenie pustego en_str który bęzdie przechowywał string bez polskich znaków
    en_str = ""
    # Przechowuje czy znak został dodany jako przemieniony
    char_added = False

    # Celem tego całego bloku jest przejście przez każdy znak w message.content i zamienienie polskich znaków takich jak 'ą' i 'ć' na ich odpowiedniki, czyli w tym przypadku 'a' i 'c'
    # Jest to przydatne inaczej trzeba sprawdzać dwie opcje wiadomości na przykład 'zły' i 'zly', po zamianie natomiast trzeba sprawdzać tylko 'zly'
    # Iteruje przez każdy znak z pl_str
    for char in pl_str:
        # Iteruje przez każdy znak w dzienniku polskie_znaki
        for symbol in polish_symbols:
            # Jeżeli aktualny znak z dzienniku jest równy char z contentu wiadomości to go zamieniamy
            if symbol == char:
                en_str = en_str + polish_symbols[symbol]
                # Skoro został dodany znak to znak_dodany = True, aby na przykład nie zmienić 'ą' na 'a' i potem też dodać 'ą'
                char_added = True
        # Jeżeli char z contentu nie został znaleziony w dzienniku to normalny znak zostaje dodany do content
        if not char_added:
            en_str = en_str + char
        # Na końcu trzeba powrócić znak_dodany do False aby w następnej iteracji głównego for wszystko działało poprawnie
        char_added = False
    
    return en_str